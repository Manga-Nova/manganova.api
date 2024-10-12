import aioboto3

from src.settings import Settings


class AwsContext:
    """AWS context.

    Asynchronously create and get the AWS session.
    """

    _session: aioboto3.Session | None = None

    @staticmethod
    def get_session() -> aioboto3.Session:
        """Get the session."""
        if AwsContext._session is None:
            return AwsContext.create_session()
        return AwsContext._session

    @staticmethod
    def create_session() -> aioboto3.Session:
        """Create the session."""
        if AwsContext._session is not None:
            err_msg = (
                "Session is already set. "
                "Use `AwsContext.get_session()` to get the session."
            )
            raise ValueError(err_msg)

        AwsContext._session = aioboto3.Session(
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION,
        )
        return AwsContext._session
