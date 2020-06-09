# E-commerce com Django e Python

#### Aplicação de uma loja virtual simples usando Bootstrap4 no frontend e Python com Django no backend

## Tecnologias utilizadas
- Para esse projeto, foi usado um frontend baseado em Bootstrap, visto que houve um foco maior no backend e na funcionalidade de aplicação
- Django Framework
  - Permite a construção facilitada de uma área administrativa, que pode ser customizada de acordo com as necessidades da aplicação
  - Já vem com models de autenticação que contam com criptografia das senhas
  - Conta com um ótimo sistema de template, possibilitando o uso de filtros built-ins e novos que podem ser criados pelo desenvolvedor
  - O projeto pode ser divido em apps, que lidam com partes diferentes da aplicação
 
## Funcionamento da aplicação
### Foram criados 3 apps
1. Profiles: Lida com o *cadastro*, *login* e *atualização* de usuários
   - **Models**
      - Address: um usuário pode ter diversos endereços, tendo a possibilidade de atualização e adição de novos endereços
      - UserProfile: registra dados que não estão no model padrão de User do Django, como data de nascimento e CPF
        - Nesse model, há a validação matemática do CPF
   - Foram criados formulários para esses models, que também contam com validação de dados
2. Products: Lida com a *listagem de produtos*, *carrinho de compras* e *informações* sobre o pedido
    - **Models**
      - Product: guarda dados como o preço a ser mostrado e as descrição geral do produto
      - Variarion: um produto pode ter várias variações, são aquelas que serão realmente vendidas
    - **Carrinho**
      - O carrinho é armazenado na sessão em forma de JSON
3. Order: Lida com o *registro do pedido* na base de dados e o *gerenciamento dos pedidos* feitos por cada cliente
    - **Models**
      - Order: Armezana os itens do pedido, guarda a data do pedido e o preço total
      - OrderItem: Guarda as variações que compoem certo pedido
      - Foram feitos models separados para que uma mudança no e-commerce depois da compra do usuário não altere o seu pedido
      
    
