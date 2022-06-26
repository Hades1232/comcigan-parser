# Python Sample

import comcigan_parser
import asyncio

async def main():
  class_name = Timetable()
  await class_name.get_basic_info()
  await class_name.search_school("경기")
  code = await class_name.get_school_name("경기고등학교", "서울")
  await class_name.set_school(code)
  await class_name.get_data()
  timetable_data = await class_name.get_timetable()[0]
  print(timetable_data['1']['1'])

asyncio.run(main())
