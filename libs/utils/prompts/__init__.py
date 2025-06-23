from libs.utils.prompts.chat import REGISTERED_USER_FLOW_DETECTOR,NOT_REGISTERED_USER_FLOW_DETECTOR
from libs.utils.prompts.extractor import (
    BILL_PAYMENT_PROMPT,MERCHANT_PAYMENT_PROMPT,ACCOUNT_STATEMENT_PROMPT,TERM_DEPOSIT_PROMPT,ACCOUNT_DETAILS_PROMPT,TRANSFER_PROMPT,SAVING_PROMPT
)
from libs.utils.prompts.assistance import (
    QA_ASSISTANCE_PROMPT,
    SDK_ASSISTANCE_PROMPT
)


flow_detector_prompts = {
    "registered_user": REGISTERED_USER_FLOW_DETECTOR,
    "not_registered_user": NOT_REGISTERED_USER_FLOW_DETECTOR

}

extractor_prompts = {
    "pay_bills": BILL_PAYMENT_PROMPT,
    "static_merchant": MERCHANT_PAYMENT_PROMPT,
    "account_statement": ACCOUNT_STATEMENT_PROMPT,
    "term_deposit": TERM_DEPOSIT_PROMPT,
    "account_details": ACCOUNT_DETAILS_PROMPT,
    "transfer_money": TRANSFER_PROMPT,
    "savings": SAVING_PROMPT
}

assistance_prompts = {
    "qa": QA_ASSISTANCE_PROMPT,
    "sdk": SDK_ASSISTANCE_PROMPT
}
