QUERY_DESLIGAMENTO ='''
WITH afastamentos_ordenados AS (
    SELECT 
        fc.matricula,
		ps.cpf,
        fc.data_afastamento,
		ca.codigo_pmjp,
        case 
		when ca.codigo_pmjp in ('12','14') then '6'
		when ca.codigo_pmjp = '60'  then '10'
		when ca.codigo_pmjp in ('77','78','84')  then '23'
		when ca.codigo_pmjp ='79' then '24'
		when ca.codigo_pmjp in ('70','72') then '38'
		when ca.codigo_pmjp ='76' then '39'
		when ca.codigo_pmjp ='19' then '40'
		end as codigo_esocial,
		
        ca.descricao,
		
        ROW_NUMBER() OVER (
            PARTITION BY fc.matricula 
            ORDER BY fc.data_afastamento DESC
        ) AS rn
    FROM funcionario fc
    JOIN causa_afastamento ca ON ca.id_causa_afastamento = fc.id_causa_afastamento
    join pessoa ps on ps.id_pessoa = fc.id_pessoa
	WHERE fc.data_afastamento > '2024-08-01' and ca.codigo_pmjp not in ('34','91')
)
SELECT 
    matricula,
	cpf,
    data_afastamento,
    codigo_pmjp,
    descricao,
	codigo_esocial
FROM afastamentos_ordenados
WHERE rn = 1;
'''