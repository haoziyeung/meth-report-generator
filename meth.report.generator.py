#!/gpfs/users/yanghao/software/anaconda2/bin/python2.7
#coding:utf8

import sys,re,time,getopt,urllib2,urllib,json,pprint
sys.path.append('/gpfs/users/yanghao/software/anaconda2/lib/python2.7/site-packages')

usage ='''---------------------------------------------------
根据优乐编号生成血液游离DNA甲基化检测报告(docx格式)

使用方法
	./meth.report.generator.py [options]
	-h 	帮助信息
	-e 	优乐编号(必须输入)
	-p 	百分比参考分布图路径
	-t 	肺癌总百分比
	-a 	肺腺癌特异百分比
	-s 	肺鳞癌特异百分比
	-b	报告分类：1代表阳性 0代表阴性
	-o 	输出文件(例如：out.docx,必须输入)

如果有问题，请联系yanghao@eulertechnology.com
---------------------------------------------------'''

#获取用户参数
try:
	opts, args = getopt.getopt( sys.argv[1:], 'he:p:t:a:s:o:b:', [] )
except Exception,e:
	print str(e)
	print usage
	sys.exit(0)

euler,out_docx,picture = None,None,None
total_frac,adeno_frac,squa_frac = '','',''
boolean = False
for opt,val in opts:
	if opt == '-h':
		print usage
		sys.exit(0)
	if opt == '-e':
		euler = val
	if opt == '-p':
		picture = val
	if opt == '-t':
		total_frac = val
	if opt == '-a':
		adeno_frac = val
	if opt == '-s':
		squa_frac = val
	if opt == '-o':
		out_docx = val
	if opt == '-b':
		if val == str(1):
			boolean = True

if not euler:
	print '请输入优乐编号'
	print usage
	sys.exit(1)
if not out_docx:
	print '请指定输出文件路径，例如 /your/path/demo.docx'
	print usage
	sys.exit(1)

#根据用户提供的优乐编号，去获取基本信息
try:
	post_data  = urllib.urlencode({})
	req = urllib2.urlopen('http://e-project.leanapp.cn/api/project/findUserInfo/' + euler, post_data)
	response = json.loads(req.read())
except:
	response = None

#pprint.pprint(response)


#生成报告
from docxtpl import *
from docx import *
from docx.shared import Mm, Inches, Pt
reload(sys)
sys.setdefaultencoding('utf8')


result_explain = '测试富文本\n是多少的方式'
hospital = response['department'] if response.has_key('department') else ''
doctor = ''
department = ''
clinical_number = ''
client_name = response['name'] if response.has_key('name') else ''
client_number = response['mobile'] if response.has_key('mobile') else ''
client_address = ''
report_date = time.strftime("%Y-%m-%d", time.localtime())
patient_name = client_name
sex = response['gender'] if response.has_key('gender') else ''
age = response['age'] if response.has_key('age') else ''
hgt = ''
wht = ''
smoke_history = ''
receive_date = str(response['sendTime']) if response.has_key('sendTime') else ''
barcode = response['eulerNumber'] if response.has_key('eulerNumber') else ''
sampleNumber = response['sampleNumber'] if response.has_key('sampleNumber') else ''
cfdna = 'ng/ml'
report_advice = '检测到肿瘤甲基化信号，请谨遵医生建议，进行临床确诊接收临床诊疗方案' if boolean else '未检测到肿瘤甲基化信号，请谨遵医嘱做好随访和年度筛查工作'
report_date_1 = report_date
pic = picture if picture else '/gpfs/users/yanghao/project/meth.report.generator/demo_pic.png'

doc = DocxTemplate('/gpfs/users/yanghao/project/meth.report.generator/Methyl-report-V004-word.docx')

context = {
	'hospital' : hospital,
	'doctor':doctor,
	'department':department,
	'clinical_number':clinical_number,
	'client_name':client_name,
	'client_number':client_number,
	'client_address':client_address,
	'bgsj':report_date,
	'patient_name':patient_name,
	'sex':sex,
	'age':age,
	'hgt':hgt,
	'wht':wht,
	'smoke_history':smoke_history,
	'euler_r_d':receive_date,
	'barcode':barcode,
	'euler_id':sampleNumber,
	'cfdna':cfdna,
	'jieguomiaoshu':report_advice,
	'euler_r_d_1':report_date_1,
	't_score':total_frac,
	'a_score':adeno_frac,
	's_score':squa_frac,
	'result_explain' : R(result_explain),
	'picture':InlineImage(doc,pic,width=Mm(150),height=Mm(90)),
}
#print context
doc.render(context)
try:
	doc.save(out_docx)
	print '报告已经生成: ' + out_docx
except Exception,e:
	print str(e)
	sys.exit(1)
