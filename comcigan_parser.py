import asyncio
import json
import requests
import re
import base64
import lxml.html
import js2py # :( I'm sorry for using eval (even js) 


HEADERS = {'User-Agent': 'Mozilla/5.0'}
HOST_LINK = "http://컴시간학생.kr"


school_name = "경기"

class Timetable:
  def __init__(self):
     self.base_url = None
     self.port_url = None
     self.option = {"maxGrade" : 3}
     self.page_source = None
     self.school_ra = None
     self.sc_data = None 
     self.school_list = None
     self.weekday_string_list = ['일', '월', '화', '수', '목', '금', '토']
     self.school_code = None
     self.main_info = None

  async def get_school_name(self, school_name, city):
      json_school_list = json.loads(self.school_list)
      for items in json_school_list:
        if school_name == items[2] and city == items[1]:
          return items[3]
      
  
  async def get_basic_info(self, option = None):

      if option:
        self.option = option
         
      original_code = requests.get(HOST_LINK, headers=HEADERS)
      lower_code = original_code.text.lower().replace("'", '"')


      frame = re.search("<frame src=\"h.+\"", lower_code).group()

      port_url = re.search("h.+\"", frame).group().replace('"', "")
      # url : http://컴시간학생.kr:PORT
      
      self.port_url = port_url

      base_url = re.search("h.+/", port_url).group()
      # base_url : http://컴시간학생.kr

      self.base_url = base_url 

      sr_sd_link = requests.get(port_url, headers=HEADERS)   
      sr_sd_link.encoding = None # 한글 깨짐 방지

      self.page_source = sr_sd_link.text

      school_ra_index = sr_sd_link.text.find("school_ra(sc)")
      school_ra_text = sr_sd_link.text[school_ra_index:school_ra_index+50].replace(" ", "")
      school_ra_url = re.search("{url:'.+'", school_ra_text).group()
      school_ra = re.search("'.+", school_ra_url).group().replace("'", "").replace(".", "").replace("/", "")
      
      self.school_ra = school_ra

      sc_data_index = sr_sd_link.text.find("sc_data('")
      sc_data_text = sr_sd_link.text[sc_data_index:sc_data_index+30]
      sc_data = re.search("('.+[0-9])", sc_data_text).group().replace("()", "").replace("'", "").split(",")
     
      self.sc_data = sc_data

  async def search_school(self, school_name):
      hex_string = ''
      for i in school_name.encode('euc-kr'):
          hex_string += '%' + format(i, 'x') 

      school_list_link = requests.get(self.base_url + self.school_ra + hex_string, headers=HEADERS)
      school_list_link.encoding = None


      school_list = re.search("\[.+}", school_list_link.text).group()[:-1] # json.load() makes error (Extra Data)
      chose_school_info = json.loads(school_list)


      if len(chose_school_info) <= 0: raise Exception("입력된 학교가 존재하지 않습니다!")
      self.school_list = school_list
     

  async def set_school(self, school_code):
     self.school_code = str(school_code)
  
  async def get_data(self):
      da1 = "0"
      s7 = self.sc_data[0] + self.school_code
      sc3 = self.school_ra.split("?")[0] + "?" + str(base64.b64encode(bytearray(s7 + '_' + da1 + '_' + self.sc_data[2], "utf-8"))).replace('\'', "")[1:]#base64.b64decode('base64_string'))#memoryview(bytes(int(s7)))#s7 + '_' + da1 + '_' + sc_data[2]))

      comcigan_api_url = self.base_url + sc3

      main_api_url = requests.get(comcigan_api_url, headers=HEADERS)
      main_api_url.encoding = None

      main_info= json.loads(main_api_url.text[0:main_api_url.text.find("}")+1])

      self.main_info = main_info

  async def get_class_time(self):
    class_time = self.main_info["일과시간"]

  async def get_timetable(self): 
      main_info = self.main_info

      


      sr_sd_page_source = self.page_source
      startTag = re.search("<script language.+?>", sr_sd_page_source).group()

      regex = re.compile(startTag + "(.+)</script>")



      script = regex.search(sr_sd_page_source)[1]
      script = re.search(".+</script>", script).group()
      script = re.search(".+}", script).group()


      function_name = re.match("function 자료.+?\(", script).group()[:-1].replace("function", "").replace(" ", "")

      classCount = main_info['학급수']

      timetable_data = {}

      default_grade = 1      
      class_num = 1
      
      while default_grade <= self.option['maxGrade']:
        str_grade = str(default_grade)
        
        try:
          if not timetable_data[str_grade]: # This code won't use
            timetable_data[str_grade] = {}
        except:
          timetable_data[str_grade] = {}
        
        
          while class_num <= classCount[default_grade]:
            str_class_num = str(class_num)
            try:
              if not timetable_data[str_grade][str_class_num]: # This code won't use too 
                timetable_data[str_grade][str_class_num] = {} 
            except:
              timetable_data[str_grade][str_class_num] = {}
              timetable_data[str_grade][str_class_num] = await self.get_class_timetable({"data": str(main_info), "script" : script, "function_name": function_name},
                default_grade,
                class_num,
              )
            
            class_num +=1
            
          default_grade += 1
          class_num = 1
  
      return timetable_data

  async def get_class_timetable(self, code_config, grade, class_number):
    
   
    n_list_number = 0
    list_up_number = 0 
    blank_list_location = 0 # subject_teacher_list에서 첫 번쩨 ""는 1교시에서 2교시로 넘어갈 때를 의미
    
    args = [code_config["data"], str(grade), str(class_number)]
    
    call = code_config["function_name"] + '(' + ",".join(args) + ')'
  
    script = code_config["script"] + '\n\n ' + call
  
    
    text_code = js2py.eval_js(script) # Sry :(
  
    text = re.sub("<br>", "\n", text_code)
    html_code = lxml.html.fromstring(text)
    
    timetable = []
    subject_teacher_list = []

    
    for items in html_code.cssselect('td'):
      for classname in iter(items.classes):
        if classname == "변경" or classname == "내용":
          text = items.text_content()
          split_text = text.split("\n")
            
          if split_text[0] == "": 
              subject, teacher = "", ""
              if blank_list_location == 0: blank_list_location = len(subject_teacher_list) + 1
        

          else : subject, teacher = split_text[0], split_text[1]        
          subject_teacher_list.append({"subject" : subject, "teacher" : teacher})
    
    n_list = [blank_list_location *i for i in range(len(subject_teacher_list) // blank_list_location)]

    for time_idx in range(len(html_code.cssselect('tr'))):
    
    
      current_time = time_idx - 2
      
      if time_idx <= 1: continue

      td_element = html_code.cssselect('td')
      
    
      list_up_number = 0
      for week_day_idx in range(len(td_element)):
        
      
        currentWeekDay = week_day_idx - 1

      
        if week_day_idx == 0: continue
        elif week_day_idx == 6: break

        teacher = subject_teacher_list[n_list[n_list_number] + list_up_number]["teacher"]
        subject = subject_teacher_list[n_list[n_list_number] + list_up_number]["subject"]
        
        timetable_dict = {
          "grade" : grade,
          "class": class_number,
          "weekday": week_day_idx - 1,
          "weekday_string": self.weekday_string_list[week_day_idx],
          "class_time": current_time + 1,
          "teacher" : teacher,
          "subject" : subject,
          }
        
        
        if current_time == 0: timetable.append([timetable_dict])
        else: timetable[currentWeekDay].append(timetable_dict)
        
        list_up_number += 1

      if n_list_number == len(n_list) - 1: n_list_number=0
      else: n_list_number+=1
    return timetable
  
   
