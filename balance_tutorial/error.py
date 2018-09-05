from plug.error import PlugException
from plug.error import VerificationError

# Define your plugin's errors here.
class NotEnoughMoneyError(VerificationError):
    fqdn = "tutorial.error.NotEnoughMoneyError"
    status_code = 400


class InvalidAmountError(VerificationError):
    fqdn = "tutorial.error.InvalidAmountError"
    status_code = 400
