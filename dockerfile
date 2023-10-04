FROM mcr.microsoft.com/mssql/server:2019-latest

COPY ./init.sql /tmp/init.sql

HEALTHCHECK --interval=10s --retries=10 CMD /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q "SELECT 1"
