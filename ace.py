import main

main.navigate_url("https://www.acehardware.com/departments/outdoor-living/grills-and-smokers/gas-grills/8017320")

main.halt_execution(3)

main.popup_click_btn('#add-to-cart')

main.popup_click_btn('.added-to-cart-popover-buttons .checkout')

main.halt_execution(3)

main.input_text({'#coupon-code-field #coupon-code': 'couponCode'})

main.click_btn(['#cart-coupon-code'])

print("Everything worked headless!")