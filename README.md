# comcigan-parser.python

📘🕘 본 라이브러리는 `Python` 환경에서 사용할 수 있는 컴시간 알리미 시간표 파싱 라이브러리 입니다.  
본 라이브러리는 [컴시간](http://컴시간학생.kr) 홈페이지에서 등록된 학교의 **시간표** 데이터를 파싱하여 제공합니다.


## 기능

- 학교명 입력 후 바로 사용 가능
- 학급 시간표 데이터 제공

## 정보

https://github.com/leegeunhyeok/comcigan-parser 컨버팅 프로젝트입니다.

## 설치하기

컴시간 서비스를 사용하는 학교의 시간표 데이터를 쉽게 수집하여 사용할 수 있습니다.

컴시간측의 소스코드 변경으로 인해 시간표 데이터 파싱이 불가능 할 수 있습니다.


> (주의!) 본 라이브러리는 비공식적으로 컴시간 서비스의 데이터를 파싱하며, 상업적인 용도로 사용하다 문제가 발생할 경우 본 라이브러리 개발자는 책임을 지지 않습니다.



## 개발 문서

### Timetable

Timetable 클래스의 인스턴스를 생성하여 사용합니다.

모듈을 불러오면 Timetable 클래스의 인스턴스를 생성할 수 있습니다.

```python
import comcigan_parser
timetable = comcigan_parser.Timetable()
```

---

### Timetable.get_basic_info()

Api 사용에 필요한 기본적인 정보들을 가져옵니다.


```python
await timetable.get_basic_info()
```

| Parameter |  Type  | Required |
| :-------- | :----: | :------: |
| option    | object |    X     |

옵션 정보는 아래 표 참고

| Option   | Value  | default | Required |
| :------- | :----: | :-----: | :------: |
| maxGrade | number |    3    |    X     |


- `maxGrade`: 최대 학년을 지정합니다. (초등: 6, 중/고등: 3)


Return - None

---

### Timetable.search_school()

학교 정보를 검색합니다.

> 컴시간에 등록된 학교가 아닐 경우 검색되지 않습니다.

```python
await timetable.search_school(keyword)
```

| Parameter |  Type  | Required |
| :-------- | :----: | :------: |
| keyword   | string |    O     |

Return - None

### Timetable.get_school_name()

컴시간에 등록되어있는 학교를 검색하여 결과를 반환합니다.

> 검색 결과가 없는 경우 예외가 발생합니다.

```python
await timetable.get_school_name("광명경영회계고등학교", "경기")
```

| Parameter |  Type  | Required |
| :-------- | :----: | :------: |
| "광명경영회계고등학교"  | string |    O     |
| "경기"  | string |    O     |

Return - school_code(int)

### Timetable.set_school()

시간표를 불러올 학교를 지정합니다. 학교 코드는 학교 검색을 통해 확인할 수 있습니다.

```python
await timetable.set_school(school_code)
```

| Parameter |  Type  | Required |
| :-------- | :----: | :------: |
| keyword   | number |    O     |

Return - None

---



### Timetable.get_timetable()

지정한 학교의 시간표 데이터를 불러옵니다.

```python 
await timetable.get_timetable()
```

Return - `timetable{}`

---

### Timetable.get_class_time()

각 교시별 수업 시작/종료 시간정보를 반환합니다.

```python
await timetable.get_class_time()
```

Return - `string[]`

---

## 사용 방법

### Timetable 인스턴스 생성

`comcigan_parser` 모듈을 불러온 후 인스턴스를 생성합니다.  




```python
import comcigan_parser
timetable = comcigan_parser.Timetable()
```

---

### 학교 검색

컴시간에 등록되어있는 학교를 검색하여 결과를 반환합니다.

> 검색 결과가 없는 경우 예외가 발생합니다.

```python
  school_list = await timetable.search('광명')
  # school_list
  # [
  #   { _: 24966, region: '경기', name: '광명북중학교', code: 74350 },
  #   { _: 24966, region: '경기', name: '광명경영회계고등학교', code: 13209 },
  #   { _: 24966, region: '경기', name: '광명북고등학교', code: 36854 },
  #   { _: 24966, region: '경기', name: '광명고등학교', code: 31443 },
  #   { _: 24966, region: '경기', name: '광명중학교', code: 31098 }
  # ]

```

---

### 학교 설정

컴시간에 등록되어있는 학교를 검색하고 인스턴스에 등록합니다.

> 학교가 여러개 조회되거나 검색 결과가 없는 경우 예외가 발생합니다.

```python
school_code = await timetable.get_search_name('광명경영회계고등학교', '경기')
await timetable.set_school(school_code)
```

---

### 시간표 조회

등록한 학교의 시간표 데이터를 조회합니다.

```python
  result = await timetable.get_timetable()
  print(result)

  # result[학년][반][요일][교시]
  # 요일: (월: 0 ~ 금: 4)
  # 교시: 1교시(0), 2교시(1), 3교시(2)..
  # 3학년 8반 화요일 2교시 시간표
  print(result[3][8][1][1])

```

---

### 수업시간 정보 조회

수업 시간 정보를 반환힙니다.

```python
await timetable.get_class_time()
```

---

## 활용 예시

```python
import comcigan_parser
timetable = comcigan_parser.Timetable()

await class_name.get_basic_info()
await class_name.search_school("광명")
code = await class_name.get_school_name("광명경영회계고등학교", "경기")
await class_name.set_school(code)
await class_name.get_data()
res = await class_name.get_timetable()
print(res[0]) # 시간표
print(res[1]) # 수업시간정보

```

```javascript
const Timetable = require('comcigan-parser');
const timetable = new Timetable();

const test = async () => {
  await timetable.init();
  const school = await timetable.search('광명경영회계고등학교');
  timetable.setSchool(school[0].code);

  // 전교 시간표 정보 조회
  const result = await timetable.getTimetable();
  console.log(result);

  // 각 교시별 수업 시작/종료 시간 정보 조회
  const time = await timetable.getClassTime();
  console.log(time);
};
```

## 데이터 형식

### 학교 데이터

```python
{
  _: 24966, // 알 수 없는 코드
  region:'경기', // 지역
  name: '광명경영회계고등학교', // 학교명
  code: 13209 // 학교코드
}
```

### 시간표 데이터

```python
{
  "1": {
    # 1학년
    "1": [ # 1반
      [ # 월요일 시간표
        {
          grade: 1,                   # 학년
          class: 1,                   # 반
          weekday: 1,                 # 요일 (1: 월 ~ 5: 금)
          weekdayString: '월',         # 요일 문자열
          classTime: 1,              # 교시
          teacher: '이희*',            # 선생님 성함
          subject: '실용비즈니스영어'     # 과목명
        },
        {
          grade: 1,
          class: 1,
          weekday: 1,
          weekdayString: '월',
          classTime: 2,
          code: '1606',
          teacher: '강연*',
          subject: '진로활동'
        }
      ],
      [화요일시간표],
      [수요일시간표],
      [목요일시간표],
      [금요일시간표]
    ],
    "2": [ # 2반
      [월요일시간표],
      [화요일시간표],
      [수요일시간표],
      [목요일시간표],
      [금요일시간표]
    ],
    "3": [
      [], [], [], [], []
    ],
    ...
  },
  "2": {
    # 2학년
  },
  "3": {
    # 3학년
  }
}
```

각 시간표 데이터 형식

- 각 요일 `Array` 에는 아래와 같은 형식의 데이터가 포함되어있음

```python
[
  {
    grade: 3,                   # 학년
    class: 10,                  # 반
    weekday: 1,                 # 요일 (1: 월 ~ 5: 금)
    weekdayString: '월',        # 요일 문자열
    classTime: 1,               # 교시
    code: '5644',               # 수업 코드
    teacher: '이희',            # 선생님 성함
    subject: '실용비즈니스영어'     # 과목명
  },
  {
    grade: 3,
    class: 10,
    weekday: 1,
    weekdayString: '월',
    classTime: 2,
    teacher: '강연',
    subject: '진로활동'
  },
  ...
]
```

### 수업시간 정보

```python
['1(09:10)', '2(10:10)', '3(11:10)', '4(12:10)', '5(13:50)', '6(14:50)', '7(15:50)', '8(16:50)'];
```

응용 방법

```python
  result = await timetable.get_timetable()
  # 3학년 8반 시간표 (월 ~ 금)
  print(result[3][8])

  # 1학년 1반 월요일 시간표
  print(result[1][1][0])

  // 2학년 5반 금요일 3교시 시간표
  print(result[2][5][4][2])
```

- 학년, 반의 경우 인덱스 상관 없이 동일하게 접근
  - 예: 1학년 3반(result[1][3]), 3학년 9반(result[3][9])
- 요일, 교시의 경우 인덱스는 0부터 시작하므로 -1 값을 통해 접근
  - 예: 월요일 3교시(result[..][..][0][2])

