# -*- coding: utf-8 -*-
import time

from seleniumwire import undetected_chromedriver as uc

# import undetected_chromedriver as uc

opts = uc.ChromeOptions()
# opts.add_argument( f'--headless' )

driver = uc.Chrome(version_main=114, options=opts, headless=True)

driver.get('https://www.baidu.com')
driver.maximize_window()

print(driver.page_source)

driver.close()