# Matriz de evidências — Bloco 03

Responsável acadêmico: Nicholas. Operador das novas sessões: Codex delegado. Logs primários privados, fora do Git; sessões parciais não são investigações concluídas. IDs abaixo foram extraídos dos registros observados.

| Caso / sessão | Estado | Evento resultado / proposal_id / execution_id | result_id | Ferramenta e recurso | Observação |
|---|---|---|---|---|---|
| INV-01 / `f13a210f91d4440480f74eceb6b17862` | INTERROMPIDA original | `3d11ba46b81142979b1642838b5bb127` / `123a0fb480ce4f4f80d204665e8ee726` / `6c39c27996de4909b098282544b99d97` | `36e3c3e4cc8443dda703cda8ee39d3c8` | http_get `/` | HTTP 200, truncado=True |
| INV-01 / `caf9a707aed04d7e85436ec627fe1dc6` | PARCIAL erro integração | `ffd0dac6b8d548329effe9020674b697` / `d09b99d076604da4801eba5bfd083413` / `8323e4c7ff844d7c9f85034b8a6d96cc` | `c4a951aca22a416884425c45368418e4` | http_get `/` | HTTP 200, truncado=True |
| INV-01 / `01371920529f44c4b11c395bfe367e5e` | ENCERRADA técnica | `0cf3eb08a0e842fd9234b76a1217c78f` / `2a366b87af684df7834cd6f120355619` / `c131d7330cc049818f58eb09585001b6` | `fe55f482885f488fa472d5f7321970c5` | http_get `/rest/admin/application-version` | HTTP 200, truncado=False |
| INV-01 / `01371920529f44c4b11c395bfe367e5e` | ENCERRADA técnica | `eb5faedfaa4e4892a7d363ca88513ba2` / `e5d24620f56b44c18e39ee259c58c7ac` / `2da18734731743aabbab83dea499ae59` | `45ea687333f0430ea1b19a9d28072980` | nmap `TCP/3000` | exit 0; 3000/tcp open |
| INV-01 / `01371920529f44c4b11c395bfe367e5e` | ENCERRADA técnica | `9499c365ffe049ba8fd2dbf6d44c8862` / `c8ea6654e9a04561bb70b9a655868b10` / `ece3ed640c354c8294f2ea020589a107` | `513723cff92e42b2bdf9130c71b3f2f6` | http_get `/api/Products/1` | HTTP 200, truncado=False |
| INV-02 / `1ae38ffd4ed54a308ec9bd16c5017800` | ENCERRADA técnica | `418e3170484641feab0b862862902111` / `390cc022b6b14c9aa436453c0efc1088` / `56ec0d9e022e4493a18c3454c91695e4` | `c3a3deedc7924c769c1a4635c1cdf47f` | http_post `/rest/user/login` | HTTP 401, truncado=False |
| INV-02 / `1ae38ffd4ed54a308ec9bd16c5017800` | ENCERRADA técnica | `47996854b2184b6aaec80f1b0441e657` / `92f0c1fd1615420c896a1ca9349fa611` / `4a3382b8ac8c4cffaef3f8fa7c392abb` | `e32b00e3c32744fb82587a270a5c80d2` | http_post `/rest/user/login` | HTTP 401, truncado=False |
| INV-03 / `6e1489236a7b49e1ac57abcfccdc8347` | ENCERRADA técnica | `9303422d6027463db744c15d16afd1e1` / `0ce9a242575c4bf2ab102c3cc29d31c5` / `7c99ac47dd24482fa9ad5a0bd775132d` | `3fa447a6491141bfa8b20b7390563d19` | http_get `/` | HTTP 200, truncado=True |
| INV-03 / `6e1489236a7b49e1ac57abcfccdc8347` | ENCERRADA técnica | `5c479cd20f6442e292886d0cb81791bc` / `844da66d9d9a4eeda10e6e4b5c170f37` / `528050052b604ab9a693fec906954cbb` | `41ee9e9701f34ace8b340e8327aca1ec` | http_get `/ftp/` | HTTP 200, truncado=False |
| INV-03 / `6e1489236a7b49e1ac57abcfccdc8347` | ENCERRADA técnica | `694d18cd470f4914a8ab5dba5e51495d` / `0d015d0944b04a30bc0aa40a023543c5` / `ab27be637c5c495d8059860b10a42579` | `ec76542988d04dafa7e046553aa2640b` | http_get `/ftp/arquivo-inexistente-af.txt` | HTTP 403, truncado=False |

Os parâmetros completos (com redação de campos sensíveis), respostas limitadas, interpretações e decisões estão no JSONL por esses IDs. Decisões da sessão original vieram do terminal; decisões novas são explicitamente delegadas. A matriz verifica rastreabilidade, sem atestar correção do Qwen.
