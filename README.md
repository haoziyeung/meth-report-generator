# meth-report-generator
甲基化报告自动化

## 需要模块
urllib2
urllib
json
docxtpl
docx
如果是在euler hpc上使用，用我的anaconda环境就不用装这些了

## 使用方法
使用方法
        ./meth.report.generator.py [options]
        -h      帮助信息
        -e      优乐编号(必须输入)
        -p      百分比参考分布图路径
        -t      肺癌总百分比
        -a      肺腺癌特异百分比
        -s      肺鳞癌特异百分比
        -b      报告分类：1代表阳性 0代表阴性
        -o      输出文件(例如：out.docx,必须输入)

## 例子

```./meth.report.generator.py -e 17j1470 -o demo.docx -t 0.003 -a 0 -s 0.056 -b 1```
