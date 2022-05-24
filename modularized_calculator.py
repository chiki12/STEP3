#! /usr/bin/python3

def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def read_times(line, index):
  token = {'type': 'TIMES'}
  return token, index + 1



def read_divide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def read_open_p(line, index):
  token = {'type': 'OPENP'}
  return token, index + 1

def read_close_p(line, index):
  token = {"type": 'CLOSEP'}
  return token, index + 1


# def tokenize(line):
#   tokens = []
#   index = 0
#   while index < len(line):
#     if line[index].isdigit():
#       (token, index) = read_number(line, index)
#     elif line[index] == '+':
#       (token, index) = read_plus(line, index)
#     elif line[index] == '-':
#       (token, index) = read_minus(line, index)
#     elif line[index] == '*':
#       (token, index) = read_times(line, index)
#     elif line[index] == "/":
#       (token, index) = read_divide(line, index)
#     else:
#       print('Invalid character found: ' + line[index])
#       exit(1)
#     tokens.append(token)
#   return tokens


# lineをtokenizeのついでに()を消す方法　　=>　でも見やすくために新しい関数を作ってevaluate（tokens)の前に（）をとるのもあり
def tokenize(line):
  tokens = []
  plist = [] #（のtokensリストのなかのインデックスが書かれている
  pcount = 0
  index = 0 # !!!!このindexはlineのインデックス
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_times(line, index)
    elif line[index] == "/":
      (token, index) = read_divide(line, index)
    elif line[index] == '(':
      (token, index) = read_open_p(line, index)
      plist.append(len(tokens)) #まだ新しいtokenがtokensリストに追加されてないので、len(tokens)は’(’のインデックス
      pcount += 1 # 今の'('のplistのなかのインデックス
    elif line[index] == ')':
      (token, index) = read_close_p(line, index) 
      #tokenは更新しても後で書き換えられるのでしなくても大丈夫ですが、indexは更新する必要ある
      pcount -= 1 #'('と対応する')'が見つかったのでpcount--1 
      store = evaluate(tokens[plist[pcount]+1:])
      del tokens[plist[pcount]:]
      del plist[pcount]
      token={'type': 'NUMBER', 'number': store}
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens




# 宿題1 
# 前の数字を記憶する変数が必要　=> store
# ＊/と会ったら、計算してtokens[index][number]にする
def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  store = 0
  # clear（）
  # # at first cycle, clear * and /
  while index < len(tokens):
    if tokens[index]['type'] == "TIMES":
      store = tokens[index-1]['number']*tokens[index+1]['number']
      tokens[index-1]={'type': 'NUMBER', 'number': store}
      del tokens[index:index+2]
    elif tokens[index]['type'] == "DIVIDE":
      store = tokens[index-1]['number']/tokens[index+1]['number']
      tokens[index-1]={'type': 'NUMBER', 'number': store}
      del tokens[index:index+2]
    else :
      index += 1 
  index = 1 #first index at the second cycle
  # do while at second cycle
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


'''    →  この部分は無視してください
# *,/だけ含む式の計算をする
def evaluate_t_d(tokens):
  answer = 1
  tokens.insert(0,{'type': 'TIMES'}) # Insert a dummy '*' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'TIMES':
        answer *= tokens[index]['number']
      elif tokens[index - 1]['type'] == 'DIVIDE':
        answer /= tokens[index]['number']
      else:
        print('Invalid syntax',answer,tokens)
        exit(1)
    index += 1
  return answer

# 式になかに*,/に会ったら、その符号だけ含む式を出して計算する
# tokenを二回するしかないかな、そしたら、計算時間が多分whileを二回するのと同じになるはず
def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  store = 0
  # do while at second cycle
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax',answer,tokens)
        exit(1)
    index += 1
  return answer
'''

def test(line):
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  test("1+1*1+2*8/4+4/2-1")
  test("0.4/1*2/1/2/1")
  test("1*2*3/4/5+1")
  test("((1+2)/3+1)+2*7")
  test("(1-2+5/1.0)*((4+4)*6)")
  test("(1.0+2.3)*(3.1-1.1)/((2.4+0)*1+2)")
  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
