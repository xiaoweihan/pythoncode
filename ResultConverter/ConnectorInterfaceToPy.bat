@echo off
REM 设置背景色和前景色
color 0A
@echo 开始进行thrift文件到Py文件的转换...
REM 设置Thrift编译器
set ThriftCompilerPath=.\thrift-0.10.0.exe
REM 设置目标文件路径
set ThriftFilePath=.\Connector.thrift
REM 设置编译标志
set ThriftCompilerFlag=-r --gen py
REM 设置thrift转换成py文件的目录
set ThriftToPyDir=.\gen-py
%ThriftCompilerPath% %ThriftCompilerFlag% %ThriftFilePath%
REM 进行文件拷贝
REM copy %ThriftToPyDir%\*.* .\JobHandler
REM copy %ThriftToCPPDir%\*.* .\NodeService
@echo 恭喜你，进行thrift文件到CPP文件的转换成功
REM rd /s /q %ThriftToPyDir%
pause