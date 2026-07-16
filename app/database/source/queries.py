QUERY_DESLIGAMENTO ='''
select distinct
	fc.matricula as matricula,
	ps.cpf as cpf,
	ca.codigo_pmjp as codigo,
	ca.descricao,
	to_char(fc.data_afastamento,'dd/MM/yyyy') as afastamento,
	'True' as COM_REMUNERACAO
		
	from rubrica_calculada rc
		join ficha_financeira ff on ff.id_ficha_financeira = rc.id_ficha_financeira
		join funcionario fc on fc.id_funcionario = ff.id_funcionario
		join causa_afastamento ca on ca.id_causa_afastamento = fc.id_causa_afastamento
		join pessoa ps on ps.id_pessoa = fc.id_pessoa
		join rubrica rb on rb.id_rubrica = rc.id_rubrica
		join unidade_trabalho ut on ut.id_unidade_trabalho = fc.id_unidade_trabalho
		join secretaria sc on sc.id_secretaria = ut.id_secretaria
		join regime rg on rg.id_regime = fc.id_regime

		where
		fc.data_afastamento > '2024-08-01' and ca.codigo_pmjp not in ('34','91','19')
		order by 5  


'''