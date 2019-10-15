#   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
def isElementExist(self, element):
    flag = True
    driver = self.driver
    try:
        driver.find_element_by_xpath(element)
        return flag

    except:
        flag = False
        return flag

