from PyPDF2 import PdfFileReader, PdfFileMerger

merger=PdfFileMerger()
input1=open(r"E:\数据预处理\的简历.pdf",'rb')
input2=open(r"E:\数据预处理\简历.pdf","rb")
merger.append(fileobj=input1)
merger.merge(position=2,fileobj=input2)
output=open(r"E:\数据预处理\结果.pdf",'wb')
merger.write(output)