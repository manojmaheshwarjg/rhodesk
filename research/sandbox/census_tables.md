| resource | list records | detail records | distinct field paths |
|---|---|---|---|
| accounts | 14 | 14 | 8 |
| cards | 8 | 8 | 47 |
| transactions | 72 | 72 | 22 |
| statements | 33 | 33 | 33 |
| invoicing_customers | 8 | 8 | 19 |
| invoicing_invoices | 12 | 12 | 39 |


### `accounts` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `account_name` | string | 14/14 | 0 | 14/14 | 0 | 8 | `Cash (Checking)`, `Credit Account`, `Inventory Checking`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_number_last_4` | string | 8/14 | 0 | 8/14 | 0 | 8 | `0106`, `2513`, `3214`, `3608`, `4609`, `5702`, `7301`, `9508` |
| `account_type` | string | 14/14 | 0 | 14/14 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `balance` | object | 14/14 | 0 | 14/14 | 0 | 0 |  |
| `balance.amount` | int | 14/14 | 0 | 14/14 | 0 | 6 | `0`, `1046`, `811970`, `876138`, `8711697`, `15460929` |
| `balance.currency` | string | 14/14 | 0 | 14/14 | 0 | 1 | `USD` |
| `id` | string | 14/14 | 0 | 14/14 | 0 | 14 | `30000000-0000-4000-8000-000000000001`, `30000000-0000-4000-8000-000000000002`, `30000000-0000-4000-8000-000000000003`, `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000005`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000008`, `30000000-0000-4000-8000-000000000009`, `30000000-0000-4000-8000-000000000010`, `30000000-0000-4000-8000-000000000011`, `30000000-0000-4000-8000-000000000012`, `30000000-0000-4000-8000-000000000013`, `30000000-0000-4000-8000-000000000014` |
| `routing_number_last_4` | string | 8/14 | 0 | 8/14 | 0 | 1 | `0089` |

### `cards` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `allowed_categories` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `allowed_categories[].code` | string | 1/1 | 0 | 1/1 | 0 | 1 | `5812` |
| `allowed_categories[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Eating places and restaurants` |
| `allowed_merchants` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `allowed_merchants[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Sweetgreen` |
| `billing_address` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `billing_address.city` | string | 8/8 | 0 | 8/8 | 0 | 4 | `Austin`, `Boston`, `Chicago`, `New York` |
| `billing_address.country_code` | string | 8/8 | 0 | 8/8 | 0 | 1 | `US` |
| `billing_address.postal_code` | string | 8/8 | 0 | 8/8 | 0 | 7 | `02116`, `10001`, `10005`, `10011`, `10118`, `60601`, `78701` |
| `billing_address.second_line` | string | 1/8 | 0 | 1/8 | 0 | 1 | `Floor 5` |
| `billing_address.street` | string | 8/8 | 0 | 8/8 | 0 | 8 | `1 Main St`, `10 Hudson Yards`, `100 Broadway`, `200 State St`, `350 Fifth Ave`, `45 W 18th St`, `500 Boylston St`, `88 Pine St` |
| `billing_address.subdivision` | string | 8/8 | 0 | 8/8 | 0 | 4 | `IL`, `MA`, `NY`, `TX` |
| `blocked_categories` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `blocked_categories[].code` | string | 1/1 | 0 | 1/1 | 0 | 1 | `0742` |
| `blocked_categories[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Veterinary services` |
| `blocked_merchants` | array | 1/8 | 0 | 1/8 | 0 | 0 |  |
| `blocked_merchants[].name` | string | 1/1 | 0 | 1/1 | 0 | 1 | `Petco` |
| `cardholder` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `cardholder.first_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Claire`, `Daniel`, `Emma`, `Ethan`, `Hannah`, `Lucas`, `Maya`, `Sofia` |
| `cardholder.last_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Bennett`, `Brooks`, `Martin`, `Mitchell`, `Parker`, `Rivera`, `Thompson`, `Walsh` |
| `cardholder.user_id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `10000000-0000-4000-8000-000000000001`, `10000000-0000-4000-8000-000000000002`, `10000000-0000-4000-8000-000000000003`, `10000000-0000-4000-8000-000000000004`, `10000000-0000-4000-8000-000000000006`, `10000000-0000-4000-8000-000000000007`, `10000000-0000-4000-8000-000000000008`, `10000000-0000-4000-8000-000000000009` |
| `current_spend` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `current_spend.amount` | int | 8/8 | 0 | 8/8 | 0 | 8 | `0`, `1750`, `5331`, `6331`, `6797`, `45000`, `121827`, `1622132` |
| `current_spend.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `20000000-0000-4000-8000-000000000001`, `20000000-0000-4000-8000-000000000002`, `20000000-0000-4000-8000-000000000003`, `20000000-0000-4000-8000-000000000004`, `20000000-0000-4000-8000-000000000005`, `20000000-0000-4000-8000-000000000006`, `20000000-0000-4000-8000-000000000007`, `20000000-0000-4000-8000-000000000008` |
| `last_4` | string | 8/8 | 0 | 8/8 | 0 | 8 | `0042`, `1184`, `1846`, `3150`, `6603`, `7291`, `7732`, `9027` |
| `name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh Virtual Card`, `Ethan Parker`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Sofia Martin Physical Card` |
| `pending_spend` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `pending_spend.amount` | int | 8/8 | 0 | 8/8 | 0 | 7 | `0`, `250`, `400`, `900`, `1500`, `8000`, `50000` |
| `pending_spend.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `shipping_address` | null+object | 8/8 | 4 | 8/8 | 4 | 0 |  |
| `shipping_address.city` | string | 4/4 | 0 | 4/4 | 0 | 4 | `Austin`, `Chicago`, `New York`, `San Francisco` |
| `shipping_address.country_code` | string | 4/4 | 0 | 4/4 | 0 | 1 | `US` |
| `shipping_address.postal_code` | string | 4/4 | 0 | 4/4 | 0 | 4 | `10118`, `60601`, `78701`, `94102` |
| `shipping_address.second_line` | string | 4/4 | 0 | 4/4 | 0 | 4 | `Apt 4B`, `Floor 20`, `Suite 200`, `Unit 12` |
| `shipping_address.street` | string | 4/4 | 0 | 4/4 | 0 | 4 | `1 Main St`, `200 State St`, `350 Fifth Ave`, `800 Market St` |
| `shipping_address.subdivision` | string | 4/4 | 0 | 4/4 | 0 | 4 | `CA`, `IL`, `NY`, `TX` |
| `spend_period_end` | null+string | 8/8 | 1 | 8/8 | 1 | 2 | `2026-09-10T04:00:00Z`, `2026-10-01T04:00:00Z` |
| `spend_period_start` | string | 8/8 | 0 | 8/8 | 0 | 3 | `2025-03-01T12:00:00Z`, `2026-09-01T04:00:00Z`, `2026-09-09T04:00:00Z` |
| `spending_limit` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `spending_limit.amount` | int | 8/8 | 0 | 8/8 | 0 | 7 | `75000`, `100000`, `150000`, `200000`, `250000`, `500000`, `2500000` |
| `spending_limit.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `spending_limit_type` | string | 8/8 | 0 | 8/8 | 0 | 3 | `daily`, `fixed`, `monthly` |
| `status` | string | 8/8 | 0 | 8/8 | 0 | 5 | `active`, `canceled`, `expired`, `locked`, `suspended` |
| `type` | string | 8/8 | 0 | 8/8 | 0 | 2 | `physical`, `virtual` |
| `usage_ends_at` | null+string | 8/8 | 5 | 8/8 | 5 | 2 | `2026-06-30T23:59:59Z`, `2026-09-01T00:00:00Z` |
| `usage_starts_at` | null+string | 8/8 | 7 | 8/8 | 7 | 1 | `2025-10-01T09:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `allowed_categories` | len 1 x1 |
| `allowed_merchants` | len 1 x1 |
| `blocked_categories` | len 1 x1 |
| `blocked_merchants` | len 1 x1 |

### `transactions` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `account_id` | string | 72/72 | 0 | 72/72 | 0 | 11 | `30000000-0000-4000-8000-000000000001`, `30000000-0000-4000-8000-000000000002`, `30000000-0000-4000-8000-000000000003`, `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000009`, `30000000-0000-4000-8000-000000000011`, `30000000-0000-4000-8000-000000000012`, `30000000-0000-4000-8000-000000000013`, `30000000-0000-4000-8000-000000000014` |
| `account_name` | string | 72/72 | 0 | 72/72 | 0 | 7 | `Cash (Checking)`, `Credit Account`, `Primary Checking`, `Reserve Checking`, `Rewards`, `Savings`, `Treasury Checking` |
| `account_type` | string | 72/72 | 0 | 72/72 | 0 | 4 | `checking`, `credit`, `rewards`, `savings` |
| `amount` | object | 72/72 | 0 | 72/72 | 0 | 0 |  |
| `amount.amount` | int | 72/72 | 0 | 72/72 | 0 | 64 | 64 distinct, min `-5900000` max `130000000` |
| `amount.currency` | string | 72/72 | 0 | 72/72 | 0 | 1 | `USD` |
| `attachments` | array | 72/72 | 0 | 72/72 | 0 | 0 |  |
| `attachments[].file_id` | string | 16/16 | 0 | 16/16 | 0 | 15 | `104c1de5-dcd3-429d-933e-d61fd076a55c`, `11afe478-b02d-4d88-a774-1e85b434eeee`, `1b6d9736-a62c-48ab-972c-804fb4a7210f`, `2c436c0c-5d8b-4114-aa2d-8d7bd64d9b15`, `3f33ab1e-8bb7-4d9e-baf3-633da9e49fd9`, `5557f9f5-74ea-4d12-9fb8-e6483f17c08c`, `5abcd54c-9726-412c-a315-500b007a6263`, `602581d9-13e9-4aaa-a227-55645354bdf8`, `6c086ad1-67c5-408e-b2c7-7766178b2211`, `7de7495f-e0d3-4ada-a79d-6074e745dc33`, `8191a1bf-5585-45a4-8950-381e71835547`, `8c284ea9-bbcb-4d71-8074-0f6fb93d224d`, `8d073098-e509-4fe3-940b-ab22de36fe7a`, `af1456af-1428-4845-8b03-9c98e098ec18`, `cdc328c1-c3a3-4670-a371-28e34891ee68` |
| `attachments[].file_name` | string | 16/16 | 0 | 16/16 | 0 | 15 | `car-service-itinerary.pdf`, `car-service-receipt.pdf`, `checking-repayment-confirmation.pdf`, `cloudbridge-invoice.pdf`, `credit-repayment-receipt.pdf`, `credit-repayment-statement.pdf`, `credit-repayment-summary.pdf`, `office-supply-invoice.pdf`, `office-supply-receipt.pdf`, `parking-receipt.pdf`, `repayment-confirmation.pdf`, `repayment-details.csv`, `rewards-cashback-notice.pdf`, `rewards-redemption-confirmation.pdf`, `software-invoice.pdf` |
| `card_id` | string | 12/72 | 0 | 12/72 | 0 | 8 | `20000000-0000-4000-8000-000000000001`, `20000000-0000-4000-8000-000000000002`, `20000000-0000-4000-8000-000000000003`, `20000000-0000-4000-8000-000000000004`, `20000000-0000-4000-8000-000000000005`, `20000000-0000-4000-8000-000000000006`, `20000000-0000-4000-8000-000000000007`, `20000000-0000-4000-8000-000000000008` |
| `card_name` | string | 12/72 | 0 | 12/72 | 0 | 8 | `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh Virtual Card`, `Ethan Parker`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Sofia Martin Physical Card` |
| `counterparty_name` | string | 72/72 | 0 | 72/72 | 0 | 37 | 37 distinct, `Aaron Blake` … `Zurich Airport Services` |
| `id` | string | 72/72 | 0 | 72/72 | 0 | 72 | 72 distinct, `018870b5-c260-7000-8000-000000000045` … `019f0554-0bf0-7000-8000-00000000000a` |
| `initiated_at` | string | 72/72 | 0 | 72/72 | 0 | 67 | 67 distinct, `2023-05-31T07:29:00Z` … `2026-06-26T19:07:02Z` |
| `memo` | string | 39/72 | 0 | 39/72 | 0 | 25 | `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Daily credit repayment for date 2026/06/24`, `Inventory restock`, `Invoice 317 - consulting services`, `Invoice 317 - production hours`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `One day Credit refund for date: 2024-03-19 00:00:28.648131-04:00`, `PAY1001984`, `PAY1002456`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `SC-2509 desk mat order`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle`, `[INVALID_RECEIVING_ROUTING_NUMBER] Vendor payment`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`, `note: Inventory purchase closing, reason: Inventory purchase closing, ref: Inventory purchase closing` |
| `money_movement_id` | string | 72/72 | 0 | 72/72 | 0 | 65 | 65 distinct, `40000000-0000-4000-8000-000000000001` … `40000000-0000-4000-8000-000000000065` |
| `note` | string | 39/72 | 0 | 39/72 | 0 | 25 | `Contractor hours`, `Correction of encoding error regarding check number 100245`, `Daily credit repayment for date 2026/06/23`, `Daily credit repayment for date 2026/06/24`, `Inventory restock`, `Invoice 317 - consulting services`, `Invoice 317 - production hours`, `MONEY TRANSFER`, `Monthly office rent`, `One day Credit refund for date: 2024-03-15 00:00:31.361435-04:00`, `One day Credit refund for date: 2024-03-19 00:00:28.648131-04:00`, `PAY1001984`, `PAY1002456`, `Q3 freight invoice`, `Rewards cashback`, `SC - 2509 - desk mat shipping`, `SC-2509 desk mat order`, `Severance payment`, `Swift OUR fee`, `Transfer to external account`, `Wire fee`, `[INVALID_RECEIVING_ROUTING_NUMBER] Payroll cycle, Error: Invalid receiving routing number.`, `[INVALID_RECEIVING_ROUTING_NUMBER] Vendor payment, Error: Invalid receiving routing number.`, `note: C-10001 merchandise order, reason: GOODS_AND_SERVICES, ref: C-10001 merchandise order`, `note: Inventory purchase closing, reason: Inventory purchase closing, ref: Inventory purchase closing` |
| `posted_at` | string | 71/72 | 0 | 71/72 | 0 | 65 | 65 distinct, `2023-05-31T07:30:00Z` … `2026-06-27T19:13:15Z` |
| `status` | string | 72/72 | 0 | 72/72 | 0 | 4 | `awaiting_approval`, `failed`, `pending`, `settled` |
| `transaction_type` | string | 72/72 | 0 | 72/72 | 0 | 22 | `ach_credit`, `ach_debit`, `ach_return`, `adjustment_credit`, `adjustment_debit`, `card_debit`, `card_refund`, `check_deposit`, `check_payment`, `credit_repayment`, `credit_repayment_refund`, `internal_transfer`, `international_wire_fee`, `international_wire_out`, `rewards_accrual`, `rewards_cashback_redemption`, `savings_deposit`, `savings_interest`, `savings_withdrawal`, `wire_fee`, `wire_in`, `wire_out` |
| `user_full_name` | string | 38/72 | 0 | 38/72 | 0 | 12 | `Andrew Collins`, `Claire Mitchell`, `Daniel Rivera`, `Emma Walsh`, `Ethan Parker`, `Grace Morgan`, `Hannah Brooks`, `Lucas Bennett`, `Maya Thompson`, `Olivia Chen`, `Priya Shah`, `Sofia Martin` |
| `user_id` | string | 38/72 | 0 | 38/72 | 0 | 12 | `10000000-0000-4000-8000-000000000001`, `10000000-0000-4000-8000-000000000002`, `10000000-0000-4000-8000-000000000003`, `10000000-0000-4000-8000-000000000004`, `10000000-0000-4000-8000-000000000005`, `10000000-0000-4000-8000-000000000006`, `10000000-0000-4000-8000-000000000007`, `10000000-0000-4000-8000-000000000008`, `10000000-0000-4000-8000-000000000009`, `10000000-0000-4000-8000-000000000010`, `10000000-0000-4000-8000-000000000011`, `10000000-0000-4000-8000-000000000012` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `attachments` | len 0 x58, len 1 x12, len 2 x2 |

### `statements` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `accounts` | array | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].account_id` | string | 33/33 | 0 | 33/33 | 0 | 5 | `30000000-0000-4000-8000-000000000004`, `30000000-0000-4000-8000-000000000006`, `30000000-0000-4000-8000-000000000007`, `30000000-0000-4000-8000-000000000008`, `30000000-0000-4000-8000-000000000013` |
| `accounts[].account_type` | string | 33/33 | 0 | 33/33 | 0 | 4 | `checking`, `credit`, `savings`, `treasury` |
| `accounts[].cashback` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].cashback.amount` | int | 22/22 | 0 | 22/22 | 0 | 19 | `-327`, `-1`, `0`, `25`, `27`, `37`, `63`, `75`, `82`, `231`, `258`, `272`, `282`, `470`, `760`, `1039`, `32482`, `78857`, `103965` |
| `accounts[].cashback.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].closing_balance` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].closing_balance.amount` | int | 33/33 | 0 | 33/33 | 0 | 14 | `0`, `1700`, `18910`, `24410`, `39810`, `90522`, `109322`, `127480`, `972409`, `985900`, `5384647`, `5453868`, `7550175`, `12315685` |
| `accounts[].closing_balance.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].opening_balance` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].opening_balance.amount` | int | 33/33 | 0 | 33/33 | 0 | 13 | `0`, `1700`, `18910`, `24410`, `39810`, `90522`, `109322`, `127480`, `946209`, `991900`, `5384647`, `5453868`, `7550175` |
| `accounts[].opening_balance.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].repayments` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].repayments.amount` | int | 22/22 | 0 | 22/22 | 0 | 10 | `-2165638`, `-69221`, `-37600`, `-6000`, `-5100`, `-3000`, `-2191`, `0`, `100`, `26200` |
| `accounts[].repayments.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].spending` | object | 22/33 | 0 | 22/33 | 0 | 0 |  |
| `accounts[].spending.amount` | int | 22/22 | 0 | 22/22 | 0 | 19 | `-26200`, `-100`, `0`, `1700`, `2191`, `3000`, `5100`, `5500`, `6000`, `15400`, `17210`, `18158`, `18800`, `37600`, `50712`, `69331`, `2165528`, `5257167`, `6931038` |
| `accounts[].spending.currency` | string | 22/22 | 0 | 22/22 | 0 | 1 | `USD` |
| `accounts[].total_credits` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_credits.amount` | int | 33/33 | 0 | 33/33 | 0 | 2 | `0`, `26200` |
| `accounts[].total_credits.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].total_debits` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_debits.amount` | int | 33/33 | 0 | 33/33 | 0 | 2 | `0`, `6000` |
| `accounts[].total_debits.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `accounts[].total_fees` | object | 33/33 | 0 | 33/33 | 0 | 0 |  |
| `accounts[].total_fees.amount` | int | 33/33 | 0 | 33/33 | 0 | 1 | `0` |
| `accounts[].total_fees.currency` | string | 33/33 | 0 | 33/33 | 0 | 1 | `USD` |
| `available_at` | string | 33/33 | 0 | 33/33 | 0 | 32 | 32 distinct, `2024-08-01T04:02:00Z` … `2026-06-05T21:16:51Z` |
| `id` | string | 33/33 | 0 | 33/33 | 0 | 33 | 33 distinct, `152980` … `572981` |
| `pdf_url` | string | 33/33 | 0 | 33/33 | 0 | n/a | signed GCS URL, see §PDF analysis |
| `period_end` | string | 33/33 | 0 | 33/33 | 0 | 29 | `2024-07-31`, `2024-08-31`, `2024-09-30`, `2024-10-31`, `2024-11-30`, `2024-12-31`, `2025-01-31`, `2025-02-28`, `2025-03-31`, `2025-04-30`, `2025-05-31`, `2025-06-12`, `2025-07-12`, `2025-08-12`, `2025-09-12`, `2025-10-12`, `2025-11-12`, `2025-11-30`, `2025-12-12`, `2025-12-31`, `2026-01-12`, `2026-01-31`, `2026-02-12`, `2026-02-28`, `2026-03-12`, `2026-03-31`, `2026-04-12`, `2026-04-30`, `2026-05-31` |
| `period_start` | string | 33/33 | 0 | 33/33 | 0 | 29 | `2024-07-01`, `2024-08-01`, `2024-09-01`, `2024-10-01`, `2024-11-01`, `2024-12-01`, `2025-01-01`, `2025-02-01`, `2025-03-01`, `2025-04-01`, `2025-05-01`, `2025-05-13`, `2025-06-13`, `2025-07-13`, `2025-08-13`, `2025-09-13`, `2025-10-13`, `2025-11-01`, `2025-11-13`, `2025-12-01`, `2025-12-13`, `2026-01-01`, `2026-01-13`, `2026-02-01`, `2026-02-13`, `2026-03-01`, `2026-03-13`, `2026-04-01`, `2026-05-01` |
| `statement_type` | string | 33/33 | 0 | 33/33 | 0 | 3 | `account`, `credit`, `treasury` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `accounts` | len 1 x33 |

### `invoicing_customers` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `address` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `address.address1` | string | 8/8 | 0 | 8/8 | 0 | 8 | `1 Contoso Way`, `100 Crosby St`, `12 Maple Lane`, `200 Market St`, `450 Pier Ave`, `77 Broadway`, `88 Mission St`, `9 Archive Rd` |
| `address.address2` | string | 8/8 | 0 | 8/8 | 0 | 3 | `<empty string>`, `Floor 2`, `Suite 400` |
| `address.city` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Austin`, `Boston`, `Chicago`, `New York`, `Portland`, `Redmond`, `San Francisco`, `Seattle` |
| `address.country` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USA` |
| `address.state` | string | 8/8 | 0 | 8/8 | 0 | 7 | `CA`, `IL`, `MA`, `NY`, `OR`, `TX`, `WA` |
| `address.zip_code` | string | 8/8 | 0 | 8/8 | 0 | 8 | `02109`, `10012`, `60601`, `78701`, `94105`, `97201`, `98052`, `98101` |
| `cc_emails` | array | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `created_at` | string | 8/8 | 0 | 8/8 | 0 | 8 | `2026-01-10T09:00:00Z`, `2026-01-15T10:00:00Z`, `2026-02-01T09:30:00Z`, `2026-02-20T14:00:00Z`, `2026-03-05T16:45:00Z`, `2026-03-18T11:00:00Z`, `2026-04-01T08:00:00Z`, `2026-04-12T13:20:00Z` |
| `deleted_at` | null+string | 8/8 | 7 | 8/8 | 7 | 1 | `2026-05-01T12:00:00Z` |
| `email` | null+string | 8/8 | 1 | 8/8 | 1 | 7 | `accounts@orbitmedia.co`, `billing@harborlogistics.com`, `contact@summitanalytics.io`, `gone@deletedco.example`, `hello@brightleaf.design`, `info@acmesupplies.com`, `orders@northwind.example` |
| `id` | string | 8/8 | 0 | 8/8 | 0 | 8 | `60000000-0000-4000-8000-000000000001`, `60000000-0000-4000-8000-000000000002`, `60000000-0000-4000-8000-000000000003`, `60000000-0000-4000-8000-000000000004`, `60000000-0000-4000-8000-000000000005`, `60000000-0000-4000-8000-000000000006`, `60000000-0000-4000-8000-000000000007`, `60000000-0000-4000-8000-000000000008` |
| `last_invoice_id` | null+string | 8/8 | 1 | 8/8 | 1 | 7 | `70000000-0000-4000-8000-000000000002`, `70000000-0000-4000-8000-000000000003`, `70000000-0000-4000-8000-000000000006`, `70000000-0000-4000-8000-000000000008`, `70000000-0000-4000-8000-000000000010`, `70000000-0000-4000-8000-000000000011`, `70000000-0000-4000-8000-000000000012` |
| `legal_name` | string | 8/8 | 0 | 8/8 | 0 | 8 | `Acme Supplies`, `Brightleaf Design`, `Cedar & Co`, `Deleted Co`, `Harbor Logistics LLC`, `Northwind Traders`, `Orbit Media Group`, `Summit Analytics` |
| `note` | null+string | 8/8 | 4 | 8/8 | 4 | 4 | `Large volume account`, `Preferred Net 30 customer`, `Quarterly retainer`, `Soft-deleted fixture customer` |
| `total_revenue` | object | 8/8 | 0 | 8/8 | 0 | 0 |  |
| `total_revenue.amount` | int | 8/8 | 0 | 8/8 | 0 | 5 | `0`, `5000`, `43400`, `108403`, `156750` |
| `total_revenue.currency` | string | 8/8 | 0 | 8/8 | 0 | 1 | `USD` |
| `updated_at` | string | 8/8 | 0 | 8/8 | 0 | 8 | `2026-04-01T08:00:00Z`, `2026-05-01T12:00:00Z`, `2026-06-30T10:00:00Z`, `2026-06-30T17:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-10T12:30:00Z`, `2026-07-18T09:00:00Z`, `2026-07-24T16:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `cc_emails` | len 0 x4, len 1 x2, len 2 x2 |

### `invoicing_invoices` field census

`present` = occurrences of the key / occurrences of its containing object. A ratio below 1.0 means the key is **omitted** (not null) on some records.

| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |
|---|---|---|---|---|---|---|---|
| `accounting_sync_status` | string | 12/12 | 0 | 12/12 | 0 | 5 | `error`, `not_pushed`, `object_changed`, `skip`, `synced` |
| `accounting_synced_at` | null+string | 12/12 | 5 | 12/12 | 5 | 7 | `2026-01-20T10:00:00Z`, `2026-05-18T00:07:03Z`, `2026-05-20T09:00:00Z`, `2026-06-21T20:00:00Z`, `2026-06-28T16:00:00Z`, `2026-07-18T09:00:00Z`, `2026-07-24T11:00:00Z` |
| `activities` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `activities[].activity_type` | string | 44/44 | 0 | 44/44 | 0 | 11 | `accounting_synced`, `cancelled`, `card_payment_received`, `created`, `downloaded`, `marked_as_paid`, `marked_as_unpaid`, `matched`, `payment_accounting_synced`, `reminder_sent`, `sent` |
| `activities[].created_at` | string | 44/44 | 0 | 44/44 | 0 | 40 | 40 distinct, `2026-01-15T10:00:00Z` … `2026-07-24T11:00:00Z` |
| `activities[].emails` | array | 44/44 | 0 | 44/44 | 0 | 0 |  |
| `activities[].user_id` | null+string | 44/44 | 12 | 44/44 | 12 | 3 | `40000000-0000-4000-8000-000000000001`, `40000000-0000-4000-8000-000000000002`, `40000000-0000-4000-8000-000000000003` |
| `created_at` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-01-15T10:00:00Z`, `2026-01-16T14:32:07Z`, `2026-05-01T09:15:00Z`, `2026-05-01T10:00:00Z`, `2026-05-10T12:00:00Z`, `2026-05-15T08:00:00Z`, `2026-06-01T11:00:00Z`, `2026-06-20T15:00:00Z`, `2026-06-30T10:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-01T14:32:07Z`, `2026-07-10T09:00:00Z` |
| `customer` | object | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `customer.id` | string | 12/12 | 0 | 12/12 | 0 | 7 | `60000000-0000-4000-8000-000000000001`, `60000000-0000-4000-8000-000000000002`, `60000000-0000-4000-8000-000000000003`, `60000000-0000-4000-8000-000000000004`, `60000000-0000-4000-8000-000000000005`, `60000000-0000-4000-8000-000000000007`, `60000000-0000-4000-8000-000000000008` |
| `date` | string | 12/12 | 0 | 12/12 | 0 | 10 | `2026-01-15`, `2026-01-16`, `2026-05-01`, `2026-05-10`, `2026-05-15`, `2026-06-01`, `2026-06-20`, `2026-06-30`, `2026-07-01`, `2026-07-10` |
| `discount_rate` | int | 12/12 | 0 | 12/12 | 0 | 2 | `0`, `5` |
| `due_date` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-02-01`, `2026-02-15`, `2026-05-30`, `2026-06-01`, `2026-06-09`, `2026-06-15`, `2026-07-01`, `2026-07-30`, `2026-07-31`, `2026-08-10`, `2026-08-15`, `2026-08-20` |
| `file_id` | string | 9/12 | 0 | 9/12 | 0 | 9 | `50000000-0000-4000-8000-000000000020`, `50000000-0000-4000-8000-000000000021`, `50000000-0000-4000-8000-000000000022`, `50000000-0000-4000-8000-000000000023`, `50000000-0000-4000-8000-000000000024`, `50000000-0000-4000-8000-000000000025`, `50000000-0000-4000-8000-000000000026`, `50000000-0000-4000-8000-000000000027`, `50000000-0000-4000-8000-000000000028` |
| `id` | string | 12/12 | 0 | 12/12 | 0 | 12 | `70000000-0000-4000-8000-000000000001`, `70000000-0000-4000-8000-000000000002`, `70000000-0000-4000-8000-000000000003`, `70000000-0000-4000-8000-000000000004`, `70000000-0000-4000-8000-000000000005`, `70000000-0000-4000-8000-000000000006`, `70000000-0000-4000-8000-000000000007`, `70000000-0000-4000-8000-000000000008`, `70000000-0000-4000-8000-000000000009`, `70000000-0000-4000-8000-000000000010`, `70000000-0000-4000-8000-000000000011`, `70000000-0000-4000-8000-000000000012` |
| `invoice_number` | string | 12/12 | 0 | 12/12 | 0 | 12 | `INV-2026-0001`, `INV-2026-0002`, `INV-2026-0040`, `INV-2026-0041`, `INV-2026-0043`, `INV-2026-0045`, `INV-2026-0050`, `INV-2026-0052`, `INV-2026-0060`, `INV-2026-0065`, `INV-2026-0066`, `INV-2026-0070` |
| `line_items` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `line_items[].discount_rate` | int | 16/16 | 0 | 16/16 | 0 | 2 | `0`, `5` |
| `line_items[].name` | string | 16/16 | 0 | 16/16 | 0 | 16 | `Analytics retainer - Q2`, `Brand workshop`, `Campaign production`, `Close-out fee`, `Consulting Services - January`, `Consulting Services - July`, `Design sprint`, `Discovery workshop`, `ERP connector`, `Freight services`, `Implementation hours`, `Inventory sync module`, `Onboarding fee`, `Platform license`, `Travel reimbursement`, `Warehouse integration` |
| `line_items[].quantity` | float+int | 16/16 | 0 | 16/16 | 0 | 4 | `1`, `2`, `2.5`, `3` |
| `line_items[].tax_rate` | float+int+null | 16/16 | 10 | 16/16 | 10 | 4 | `0`, `6.25`, `8.5`, `10` |
| `line_items[].total` | object | 16/16 | 0 | 16/16 | 0 | 0 |  |
| `line_items[].total.amount` | int | 16/16 | 0 | 16/16 | 0 | 15 | `5000`, `6000`, `9403`, `20000`, `22000`, `40000`, `42353`, `45000`, `76000`, `90000`, `96000`, `98000`, `100000`, `156750`, `10000000` |
| `line_items[].total.currency` | string | 16/16 | 0 | 16/16 | 0 | 1 | `USD` |
| `line_items[].unit_price` | object | 16/16 | 0 | 16/16 | 0 | 0 |  |
| `line_items[].unit_price.amount` | int | 16/16 | 0 | 16/16 | 0 | 15 | `5000`, `6000`, `8000`, `9403`, `20000`, `22000`, `40000`, `42353`, `45000`, `48000`, `50000`, `52250`, `90000`, `98000`, `5000000` |
| `line_items[].unit_price.currency` | string | 16/16 | 0 | 16/16 | 0 | 1 | `USD` |
| `note` | null+string | 12/12 | 3 | 12/12 | 3 | 9 | `Customer cancelled engagement.`, `Design sprint package.`, `Final invoice before deletion.`, `Follow up scheduled.`, `Freight + handling.`, `Net 30 terms apply.`, `Q2 analytics retainer.`, `Thanks for your business! Net 30 terms apply.`, `Wire received — confirm allocation.` |
| `payments` | array | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `payments[].external_method` | null+string | 7/7 | 2 | 7/7 | 2 | 4 | `cash`, `check`, `credit_card`, `other` |
| `payments[].paid_at` | string | 7/7 | 0 | 7/7 | 0 | 6 | `2026-01-20`, `2026-05-18`, `2026-06-21`, `2026-06-28`, `2026-07-18`, `2026-07-24` |
| `payments[].transaction_id` | null+string | 7/7 | 5 | 7/7 | 5 | 2 | `019e3868-5858-7000-8000-00000000001a`, `019eebb0-0938-7000-8000-00000000000b` |
| `payments[].type` | string | 7/7 | 0 | 7/7 | 0 | 2 | `external`, `received_in_account` |
| `status` | string | 12/12 | 0 | 12/12 | 0 | 6 | `cancelled`, `confirm_payment`, `overdue`, `paid`, `pending_payout`, `unpaid` |
| `tax_rate` | float+int | 12/12 | 0 | 12/12 | 0 | 4 | `0`, `6.25`, `8.5`, `10` |
| `total` | object | 12/12 | 0 | 12/12 | 0 | 0 |  |
| `total.amount` | int | 12/12 | 0 | 12/12 | 0 | 11 | `5000`, `22000`, `43400`, `45000`, `72200`, `96000`, `98000`, `108403`, `156750`, `158000`, `10000000` |
| `total.currency` | string | 12/12 | 0 | 12/12 | 0 | 1 | `USD` |
| `updated_at` | string | 12/12 | 0 | 12/12 | 0 | 12 | `2026-01-20T10:00:00Z`, `2026-05-10T10:00:00Z`, `2026-05-18T00:07:03Z`, `2026-05-20T09:00:00Z`, `2026-06-21T20:00:00Z`, `2026-06-28T16:00:00Z`, `2026-06-30T17:00:00Z`, `2026-07-01T08:00:00Z`, `2026-07-01T08:30:00Z`, `2026-07-18T09:00:00Z`, `2026-07-20T09:00:00Z`, `2026-07-24T16:00:00Z` |

**Array lengths**

| array path | length distribution (list surface) |
|---|---|
| `activities` | len 2 x3, len 3 x4, len 4 x2, len 5 x1, len 6 x1, len 7 x1 |
| `activities[].emails` | len 0 x32, len 1 x10, len 2 x2 |
| `line_items` | len 1 x10, len 2 x1, len 4 x1 |
| `payments` | len 0 x5, len 1 x7 |