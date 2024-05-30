from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import POSTGRES_URL, POSTGRES_SSL


conn_args = {
    #"sslmode": "verify-full",
    #"sslrootcert": POSTGRES_SSL,
}

engin = create_async_engine(POSTGRES_URL, connect_args=conn_args)
session_maker = async_sessionmaker(engin, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with session_maker() as session:
        yield session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(length=32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=200), nullable=False)

    is_admin: Mapped[bool] = mapped_column(nullable=False)

    servers: Mapped[list["Server"]] = relationship("Server", back_populates="user", cascade="all, delete", passive_deletes=True)


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user: Mapped["User"] = relationship("User", back_populates="servers", foreign_keys=[user_id])

    cloud_vm_id: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    srever_map_link: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    