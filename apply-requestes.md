
# ✅ **POST**

http://127.0.0.1:5000/materiais


```json
{
"id_material": "561538",
"locale_material": "01-03-02",
"description_material": "Estator_Bobinado"
}
```

# ✅ **DELETE**

Escolha o método DELETE.
No campo URL, digite:

```
http://127.0.0.1:5000/materiais/561538
```

# ✅ **UPDATE**

Criar uma nova requisição no Insomnia.
Escolher o método PUT.
No campo URL, digite:

```
http://127.0.0.1:5000/materiais/561538
```

(Troque 561538 pelo ID do material que deseja atualizar).
Vá até a aba Body, escolha JSON e envie os novos dados:

```json
{
  "localce_material": "02-05-08",
  "description_material": "Rotor_Revisado"
}
```