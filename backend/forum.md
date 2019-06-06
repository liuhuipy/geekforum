# geekforum表设计

### BaseModel
- is_deleted
- created_time
- end_time

### 用户(CustomUser)
- 用户名(username)
- cname
- phone
- city
- email

### 项目(Project)
- 项目名(cname)
- 英文名(name)
- Owner(owner)        foreignKey CustomUser
- 源码地址(repo_url)
- 项目首页(dash_url)
- 文档地址(document_url)
- 标签(tags)          foreignKey ProjectTag
- 开发语言(develop_language)
- 项目描述(description)

### 文章(Article)
- 标题(title)
- 作者(Author)        foreignKey CustomUser
- 标签(tags)          foreignKey ArticleTag
- 内容(description)

### 节点(Node)
- 节点名(name)
- 节点key(key)
- 创建人(creator)     foreignKey CustomUser

### 话题(Topic)
- 标题(title)
- 节点(node)          foreignKey Node
- 内容(description)   
- 作者(Author)        foreignKey CustomUser

### 评论(comment)
- 内容(content)
- parent

### 文章点赞(article_star)
- 文章(article)       foreignKey Article
- 点赞人(creator)     foreignKey CustomUser
- star_type            

### 评论点赞(star)
- 评论(comment)       foreignKey comment
- 点赞人(creator)     foreignKey CustomUser
- star_type

