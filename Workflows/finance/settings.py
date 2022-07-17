from Business import *

r_string_gcash_payment = r'Your payment of P(\d+(?:,\d+|\d+)\.?\d*) to (.+?) ' \
                         r'has been successfully processed on (.+?). Ref. No. (\d+)'

r_string_gcash_payment_store = r'You have paid P(\d+(?:,\d+|\d+)\.?\d*) of GCash to (.+?) ' \
                         r'on (.+?). Ref. No. (\d+).'

r_string_gcash_send = r'You have sent PHP (\d+(?:,\d+|\d+)\.?\d*) of GCash to (.+?) (\d+) on (.+?). ' \
                      r'Your new balance is PHP (\d+(?:,\d+|\d+)\.?\d*). Ref. No. (\d+)'

r_string_gcash_receive = r'You have received PHP (\d+(?:,\d+|\d+)\.?\d*) of GCash from (.+?) (\d+) (.+?) ' \
                         r'Your new balance is PHP (\d+(?:,\d+|\d+)\.?\d*). Ref. No. (\d+).'

r_string_gcash_receive_bank = r'You have received P (\d+(?:,\d+|\d+)\.?\d*) on (.+?) from (.+?) account ending in (.+?). ' \
                         r'Your new balance is P (\d+(?:,\d+|\d+)\.?\d*) with Ref No. (\d+). Thank you'

r_union_transfer = r'You transferred PHP (\d+(?:,\d+|\d+)\.?\d*) to (.+?) Reference No.: (\w+). Thank you for using'

r_bpi_payments = r'Your One-Time PIN is (\d+). PLEASE DO NOT SHARE IT WITH ANYONE. ' \
                 r'If you did not initiate payment of P(\d+(?:,\d+|\d+)\.?\d*) for (.+?) with Ref no. (\d+)'

r_bpi_cc_payments = r'NEVER SHARE YOUR OTP. You are about to pay PHP(\d+(?:,\d+|\d+)\.?\d*) to (.+?) ' \
                    r'with ref no. (.+?) Use OTP (\d+) only if you'

r_bpi_withdraw = r'(.+?): You have withdrawn PHP (\d+(?:,\d+|\d+)\.?\d*) ' \
                 r'from your acct xxxxxx(\d+) at (.+?) on (.+?). If you'


messages_mapping = {
    'gcash_payments': (r_string_gcash_payment, [1, 2, 4], 'debit'),
    'gcash_payments_store': (r_string_gcash_payment_store, [1, 2, 4], 'debit'),
    'gcash_send': (r_string_gcash_send, [1, 2, 6], 'debit'),
    'gcash_receive': (r_string_gcash_receive, [1, 2, 6], 'credit'),
    'gcash_receive_bank': (r_string_gcash_receive_bank, [1, 3, 6], 'credit'),
    'bpi_payments': (r_bpi_payments, [2, 3, 4], 'debit'),
    'bpi_cc_payments': (r_bpi_cc_payments, [1, 2, 3], 'debit'),
    'bpi_withdraw': (r_bpi_withdraw, [2, 1, 3], 'debit'),
    'union_transfers': (r_union_transfer, [1, 2, 4], 'debit'),

}
