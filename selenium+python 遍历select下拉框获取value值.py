'''
遍历下拉框，获取value值

因为多次需要，所以写成类方法，方便调用
'''



def is_option_value_present(self,element_id,tag_name,option_text):
        driver = self.driver
        select=driver.find_element_by_id(element_id)
        # 注意使用find_elements
        options_list=select.find_elements_by_tag_name(tag_name)
        for option in options_list:
            # print ("Value is: " + option.get_attribute("value"))
            # print ("Text is:" +option.text)
            if option_text in option.text:
                select_value=option.get_attribute("value")
                print ("option_textoption_textoption_textValue is: " + select_value)
                break
        return select_value