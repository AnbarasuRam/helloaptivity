import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp \
    import template 
    
class blogpost(db.Model):
    message = db.StringProperty(required=True)
    when = db.DateTimeProperty(auto_now_add=True)
    who = db.StringProperty()
    
class BlogUser(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

class BlogHandler(webapp.RequestHandler):
    def get(self):
        blogcontents = db.GqlQuery('Select * from blogpost ORDER BY when DESC')
        values = {'blogcontents' : blogcontents}
        self.response.out.write(template.render('helloaptivity.html',values))
    
    def post(self):
        blogcontent = blogpost(message= self.request.get('message'), who = self.request.get('blogger'))
        blogcontent.put()
        self.redirect('/yourblog')

class LoginPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('loginPage.html',{}))    
        
class SecondPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('secondPage.html',{}))   

class LoginValidate(webapp.RequestHandler):
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password') 
        number1_button = self.request.get('Login')
        number2_button = self.request.get('Register')        
        if number1_button:
            q = BlogUser.all()
            q.filter("username =",username)
            q.filter("password =",password)
            user = q.get()
            if user != None:        
                profile_values= {'name':user.username}
                self.response.out.write(template.render('helloaptivity.html', profile_values))
            else:
                values = {'message' : '"Invalid username/Password. New Users please register" :-/'}
                self.response.out.write(template.render('loginPage.html',values))                                
        else:
            blogusername = BlogUser(username= self.request.get('username'), password = self.request.get('password'))
            blogusername.put()
            values = {'message' : 'User successfully registered. Now login :)'}
            self.response.out.write(template.render('loginPage.html',values))
            #self.response.out.write("User successfully registered")
           
        
def helloaptivity():
    app = webapp.WSGIApplication(routes,debug=True)
    wsgiref.handlers.CGIHandler().run(app)
    
routes = [('/', LoginPage), 
          ('/secondPage',SecondPage), 
          ('/yourblog', BlogHandler), 
          ('/loginvalidate', LoginValidate)]

helloaptivity()

#app = webapp.WSGIApplication([(r'.*', LoginPage)], debug = True)