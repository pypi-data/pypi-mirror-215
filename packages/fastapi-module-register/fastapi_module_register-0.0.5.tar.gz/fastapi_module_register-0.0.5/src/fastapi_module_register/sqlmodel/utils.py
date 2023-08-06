from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class AsyncSession:

    @classmethod
    def init(cls, db_str: str) -> None:
        """_summary_

        Args:
            db_str (str): _description_
        """
        async_engine = create_async_engine(db_str, echo=False)
        cls.async_session = sessionmaker(async_engine, class_=AsyncSession)
    
    @classmethod
    async def gen_session(cls) -> AsyncSession:
        """_summary_

        Returns:
            AsyncSession: _description_

        Yields:
            Iterator[AsyncSession]: _description_
        """
        async with cls.async_session() as session:
            yield session
