- Django Admin panelinde model isimlerinin sonuna 's' eklenmemesi için aşağıdaki kodu kullanabilirsiniz.
- Django da veritabanı adlarını app isimlerinin eklenmemesi için `Meta` sınıfında `db_table` özelliğini kullanabilirsiniz.
- 
```python

class ModelName(models.Model):
    # model alanları

    class Meta:
        verbose_name = "Model Name"
        verbose_name_plural = "Model Names"
        db_table = 'category'
        
```

### GraphQL Authentication Middleware
- Django da GraphQL için JWT token kontrolü yapmak için `core/middleware.py` dosyasındaki `GraphQLMiddleware` sınıfını  kullanabilirsiniz.
- Bu sınıfı kullanmak için `core/settings.py` dosyasındaki `MIDDLEWARE` listesine `core.middleware.GraphQLMiddleware` ekleyiniz.
- Buradaki middleware hem `graphene` hem de `strawberry` için kullanılabilir.

#### Graphene için Permission kullanımı
```python
from graphql import GraphQLError
from functools import wraps


def control_by_user(username):
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, **kwargs):
            user = info.context.user
            if user.username != username:
                raise GraphQLError("You are not authorized to access this resource")
            return func(root, info, **kwargs)
        return wrapper
    return decorator

#Şemada kullanımı
class CategoryQuery(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)

    @control_by_user("ogztest")
    def resolve_all_categories(self, info):
        return Category.objects.all()

```




