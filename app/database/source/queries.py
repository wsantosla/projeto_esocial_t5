QUERY_DESLIGAMENTO ='''
WITH parametros AS (
    SELECT 
        -- Cria o primeiro dia do mês/ano parametrizado e adiciona 2 meses
        (MAKE_DATE(ano, mes, 1) + INTERVAL '2 month') AS data_limite
    FROM parametros_sistema
),
afastamentos_ordenados AS (
    SELECT 
        fc.matricula,
        ps.cpf,
        fc.data_afastamento,
        ca.codigo_pmjp,
        CASE 
            WHEN ca.codigo_pmjp IN ('12', '14') THEN '06'
            WHEN ca.codigo_pmjp = '60'          THEN '10'
            WHEN ca.codigo_pmjp IN ('77', '78', '84') THEN '23'
            WHEN ca.codigo_pmjp = '79'          THEN '24'
            WHEN ca.codigo_pmjp IN ('70', '72') THEN '38'
            WHEN ca.codigo_pmjp = '76'          THEN '39'
            WHEN ca.codigo_pmjp = '19'          THEN '40'
        END AS codigo_esocial,
        ca.descricao,
        ROW_NUMBER() OVER (
            PARTITION BY fc.matricula 
            ORDER BY fc.data_afastamento DESC
        ) AS rn
    FROM funcionario fc
    JOIN causa_afastamento ca ON ca.id_causa_afastamento = fc.id_causa_afastamento
    JOIN pessoa ps ON ps.id_pessoa = fc.id_pessoa
    CROSS JOIN parametros p
    WHERE fc.data_afastamento > '2024-08-01'
      -- Garante que a data não seja maior que 2 meses à frente do mês/ano do sistema
      AND fc.data_afastamento <= p.data_limite
      AND ca.codigo_pmjp NOT IN ('34', '91')
      AND NOT EXISTS (
          SELECT 1
          FROM rubrica_calculada rc
          JOIN ficha_financeira ff ON ff.id_ficha_financeira = rc.id_ficha_financeira
          JOIN funcionario fc2 ON fc2.id_funcionario = ff.id_funcionario
          JOIN parametros_sistema psis ON fc2.ano = psis.ano AND fc2.mes = psis.mes
          WHERE fc2.matricula = fc.matricula
      )
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