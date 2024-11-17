@echo off
set TIMESTAMP=%date:~-4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%  
set TIMESTAMP=%TIMESTAMP::=%  

set BACKUP_FOLDER=D:\VS Code\CourseDatabase\bookstore\backup_scripts\backups
set PGPASSWORD=b23oue

set PG_DUMP_PATH="C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"

set REMOTE_USER=qweerbecouse
set REMOTE_HOST=192.168.1.49
set REMOTE_FOLDER=/home/qweerbecouse/backup

if not exist "%BACKUP_FOLDER%" (
    echo Папка %BACKUP_FOLDER% не существует, создаём...
    mkdir "%BACKUP_FOLDER%"
)

%PG_DUMP_PATH% -U postgres -h localhost -p 5432 -F p -b -v -f "%BACKUP_FOLDER%\backup_%TIMESTAMP%.sql" course_database

scp "%BACKUP_FOLDER%\backup_%TIMESTAMP%.sql" %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_FOLDER%

if %errorlevel% equ 0 (
    echo Файл успешно передан на удалённый сервер.
) else (
    echo Ошибка при передаче файла!
)

exit