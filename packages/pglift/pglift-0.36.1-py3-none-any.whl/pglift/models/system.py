from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

import psycopg.conninfo
import pydantic
from attrs import asdict, field, frozen
from attrs.validators import instance_of
from pgtoolkit import ctl
from pgtoolkit.conf import Configuration

from .. import conf, exceptions
from .._compat import Self
from ..settings import PostgreSQLVersion, Settings
from ..util import short_version

if TYPE_CHECKING:
    from ..ctx import Context


def default_postgresql_version(ctx: "Context") -> PostgreSQLVersion:
    version = ctx.settings.postgresql.default_version
    if version is None:
        return PostgreSQLVersion(short_version(ctl.PGCtl(None).version))
    return version


@frozen
class BaseInstance:
    name: str
    version: PostgreSQLVersion = field(converter=PostgreSQLVersion)

    bindir: Path = field(init=False)
    _settings: Settings = field(validator=instance_of(Settings))

    def __attrs_post_init__(self) -> None:
        for v in self._settings.postgresql.versions:
            if self.version == v.version:
                object.__setattr__(self, "bindir", v.bindir)
                break
        else:
            raise exceptions.InvalidVersion(
                f"version '{self.version}' unsupported in site settings"
            )

    def __str__(self) -> str:
        return f"{self.version}/{self.name}"

    @property
    def qualname(self) -> str:
        """Version qualified name, e.g. 13-main."""
        return f"{self.version}-{self.name}"

    @property
    def datadir(self) -> Path:
        """Path to data directory for this instance."""
        return Path(
            str(self._settings.postgresql.datadir).format(
                version=self.version, name=self.name
            )
        )

    @property
    def waldir(self) -> Path:
        """Path to WAL directory for this instance."""
        return Path(
            str(self._settings.postgresql.waldir).format(
                version=self.version, name=self.name
            )
        )

    @property
    def dumps_directory(self) -> Path:
        """Path to directory where database dumps are stored."""
        return Path(
            str(self._settings.postgresql.dumps_directory).format(
                version=self.version, name=self.name
            )
        )

    @property
    def psqlrc(self) -> Path:
        return self.datadir / ".psqlrc"

    @property
    def psql_history(self) -> Path:
        return self.datadir / ".psql_history"

    def exists(self) -> bool:
        """Return True if the instance exists based on system lookup.

        :raises ~exceptions.InvalidVersion: if PG_VERSION content does not
            match declared version
        """
        if not self.datadir.exists():
            return False
        try:
            real_version = (self.datadir / "PG_VERSION").read_text().splitlines()[0]
        except FileNotFoundError:
            return False
        if real_version != self.version:
            raise exceptions.InvalidVersion(
                f"version mismatch ({real_version} != {self.version})"
            )
        return True

    @classmethod
    def get(cls, name: str, version: Optional[str], ctx: "Context") -> Self:
        """Return a BaseInstance object from specified name and version.

        :raises ~exceptions.InvalidVersion: if PostgreSQL executable directory
            (bindir) does not exist for specified version.
        """
        # attrs strip leading underscores at init for private attributes.
        if version is None:
            version = default_postgresql_version(ctx)
        else:
            version = PostgreSQLVersion(version)
        return cls(name, version, settings=ctx.settings)


@frozen
class Standby:
    primary_conninfo: str
    slot: Optional[str]
    password: Optional[pydantic.SecretStr]

    @classmethod
    def system_lookup(cls, instance: "PostgreSQLInstance") -> Optional[Self]:
        standbyfile = (
            "standby.signal"
            if instance.version >= PostgreSQLVersion.v12
            else "recovery.conf"
        )
        if not (instance.datadir / standbyfile).exists():
            return None
        config = instance.config()
        try:
            dsn = config["primary_conninfo"]
        except KeyError:
            return None
        assert isinstance(dsn, str), dsn
        primary_conninfo = psycopg.conninfo.conninfo_to_dict(dsn)
        try:
            password = pydantic.SecretStr(primary_conninfo.pop("password"))
        except KeyError:
            password = None
        slot = config.get("primary_slot_name")
        if slot is not None:
            assert isinstance(slot, str), slot
        return cls(
            primary_conninfo=psycopg.conninfo.make_conninfo(**primary_conninfo),
            slot=slot or None,
            password=password,
        )


@frozen
class PostgreSQLInstance(BaseInstance):
    """A bare PostgreSQL instance."""

    @classmethod
    def system_lookup(
        cls, ctx: "Context", value: Union[BaseInstance, tuple[str, Optional[str]]]
    ) -> Self:
        """Build a (real) instance by system lookup.

        :param value: either a BaseInstance object or a (name, version) tuple.

        :raises ~exceptions.InstanceNotFound: if the instance could not be
            found by system lookup.
        """
        if not isinstance(value, BaseInstance):
            try:
                name, version = value
            except ValueError:
                raise TypeError(
                    "expecting either a BaseInstance or a (name, version) tuple as 'value' argument"
                )
        else:
            name, version = value.name, value.version
        try:
            self = cls.get(name, version, ctx)
            self.exists()
        except exceptions.InvalidVersion:
            raise exceptions.InstanceNotFound(f"{version}/{name}")
        return self

    @property
    def standby(self) -> Optional[Standby]:
        return Standby.system_lookup(self)

    @classmethod
    def from_qualname(cls, ctx: "Context", value: str) -> Self:
        """Lookup for an Instance by its qualified name."""
        try:
            version, name = value.split("-", 1)
        except ValueError:
            raise ValueError(f"invalid qualified name '{value}'") from None
        return cls.system_lookup(ctx, (name, version))

    def exists(self) -> bool:
        """Return True if the instance exists and its configuration is valid.

        :raises ~pglift.exceptions.InstanceNotFound: if configuration cannot
            be read
        """
        if not super().exists():
            raise exceptions.InstanceNotFound(str(self))
        try:
            self.config()
        except FileNotFoundError as e:
            raise exceptions.InstanceNotFound(str(self)) from e
        return True

    def config(self, managed_only: bool = False) -> Configuration:
        """Return parsed PostgreSQL configuration for this instance.

        Refer to :func:`pglift.conf.read` for complete documentation.
        """
        try:
            return conf.read(self.datadir, managed_only=managed_only)
        except exceptions.FileNotFoundError:
            if managed_only:
                return Configuration()
            raise

    @property
    def port(self) -> int:
        """TCP port the server listens on."""
        return int(self.config().get("port", 5432))  # type: ignore[arg-type]


@frozen
class Instance(PostgreSQLInstance):
    """A PostgreSQL instance with satellite services."""

    services: list[Any] = field()

    @services.validator
    def _validate_services(self, attribute: Any, value: list[Any]) -> None:
        if len(set(map(type, value))) != len(value):
            raise ValueError("values for 'services' field must be of distinct types")

    @classmethod
    def system_lookup(
        cls, ctx: "Context", value: Union[BaseInstance, tuple[str, Optional[str]]]
    ) -> Self:
        pg_instance = PostgreSQLInstance.system_lookup(ctx, value)
        values = asdict(pg_instance)
        del values["bindir"]  # init=False
        # attrs strip leading underscores at init for private attributes.
        values["settings"] = values.pop("_settings")
        assert "services" not in values
        values["services"] = [
            s
            for s in ctx.hook.system_lookup(ctx=ctx, instance=pg_instance)
            if s is not None
        ]
        return cls(**values)

    S = TypeVar("S")

    def service(self, stype: type[S]) -> S:
        """Return bound satellite service object matching requested type.

        :raises ValueError: if not found.
        """
        for s in self.services:
            if isinstance(s, stype):
                return s
        raise ValueError(stype)
