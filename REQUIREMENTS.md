# Requirements traceability

Source: `rental_oop.pdf`, Appendix A, Appendix B and section 2.
Run the tests with `python -m pytest -q` from the repo folder.

| Requirement | Code location | Test |
|---|---|---|
| 2.1.1 Shop RentACar starts with 4 hatchbacks, 3 sedans, 3 SUVs | `main.py` `build_shop` | `test_s211_main_initialises_rentacar_with_initial_stock` |
| 2.1.1 Each car type sets its own daily rates | `cars.py` `Hatchback`, `Sedan`, `SUV` | `test_s211_car_subclasses_define_daily_rates` |
| 2.1.2 VIP overrides `is_vip` | `customer.py` `VIP.is_vip` | `test_s212_vip_overrides_is_vip` |
| A.2.1 Rent a car, under a week | `main.py` `rent_option`, `rental_shops.py` `get_rate` | `test_a21_rent_a_car_below_week_rate` |
| A.2.1 Rent a car, a week or more | `rental_shops.py` `get_rate` | `test_a21_rent_a_car_week_or_more_rate` |
| A.2.2 View count per type and total | `rental_shops.py` `display_stock` | `test_a22_view_available_cars_shows_counts_and_total` |
| A.2.2 View reflects rentals | `rental_shops.py` `handout_car` | `test_a22_view_available_cars_after_rental` |
| A.2.3 Return updates stock | `main.py` `return_option`, `rental_shops.py` `is_returnable` | `test_a23_return_a_car_updates_stock` |
| A.2.3 Bill is rate times days | `rental_shops.py` `get_price` | `test_a23_return_a_car_displays_bill`, `test_bill_calculation` |
| A.2.4 Exit gracefully | `main.py` `run`, `rental_shops.py` `close_shop` | `test_a24_exit_platform_gracefully` |
| A.2.5 Join loyalty programme for discount | `rental_shops.py` `upgrade_customer` | `test_a25_loyalty_join_gives_discounted_rate` |
| A.2.5 Leave loyalty programme | `rental_shops.py` `downgrade_vip_customer` | `test_a25_loyalty_leave_restores_regular_rate` |
| 2.1.3 Status change keeps the rental | `customer.py` `transfer_customer_details` | `test_a25_loyalty_change_keeps_rented_car` |
| A.3.1 Usability, clear invalid input messages | `main.py` `expected_int`, `run` | `test_a31_usability_invalid_option_message` |
| A.3.2 Performance, each operation under 10 s | `main.py` `load`, `DEFAULT_DELAY` | `test_a32_performance_operations_under_10_seconds` |
| A.3.3 Reliability, stock stays consistent | `rental_shops.py` `add_to_stock`, `is_returnable` | `test_a33_reliability_stock_consistency` |
| A.4.2 In-memory storage only | `main.py` `build_shop` | `test_a42_in_memory_storage_resets_per_session` |
| B.4.1 No car (type) available | `main.py` `rent_option` | `test_b41_no_car_type_available` |
| B.4.2 Invalid option | `main.py` `run` | `test_a31_usability_invalid_option_message` |
| B.4.3 No car to return | `main.py` `return_option` | `test_b43_no_car_to_return` |
| B.4.4 One car per customer | `main.py` `rent_option` | `test_b44_rent_one_car_per_customer` |
| 4.3 Known issue: bill uses status at return | `main.py` `return_option` | `test_s43_known_issue_bill_uses_status_at_return` |

Edge cases live in `tests/test_edge_cases.py`. They cover sold-out stock, unknown car types, zero or negative days, non-numeric input and every rate band.

## Fixes against the original code

1. `add_to_stock` put one shared car object into stock many times. Each stocked car is now a new instance.
2. Rental days of zero or below produced a zero or negative bill. The CLI now asks again.
3. Upgrade and downgrade shared one details dictionary between two accounts. The transfer now copies it.
4. `is_returnable` accepted any object for a valid type. It now checks the car class.
5. Importing `main.py` started the CLI. The menu now runs only from `main()`.
