#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os,db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)




class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class MainHandler(webapp2.RequestHandler):
    def get(self):

        from suds_memcache import Client
        url = ('http://www.ayto-santander.es:9001/services/estructura.asmx?WSDL')
        c = Client(url)

        self.response.out.write("das"+c)
        #self.render('stop.html')

    #def post(self):



class NewPostHandler(Handler):
    def render_front(self,title="",content="",):
        # n = self.request.get('n')
        # self.response.out.write("La parada solicitada es "+str(id))

       self.render('newpost.html')

        #template_values = {
        #    'id_stop': id           
        #}

        #template = jinja_environment.get_template('stops.html')

        #self.response.out.write(template.render(template_values))

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        if title and content:
            p = Post(title = title, content = content)
            p.put()
            self.redirect("/blog/"+p.key().id())
        else:
            self.render_front(title,content)


class BlogHandler(Handler):
    def get(self):
        # n = self.request.get('n')
        # self.response.out.write("La parada solicitada es "+str(id))

       self.render('blog.html')

        # template_values = {
        #     'id_stop': id           
        # }

        # template = jinja_environment.get_template('stops.html')

        # self.response.out.write(template.render(template_values))



    

    


app = webapp2.WSGIApplication([('/', MainHandler),('/rot13',Rot13Handler),('/blog',BlogHandler),('/blog/newpost',NewPostHandler)], debug=True)




def rot13(text):
    r = []
    la=ord('a')
    lz=ord('z')+1
    ua=ord('A')
    uz=ord('Z')+1
    for c in text:
        ordi=ord(c)
        if ordi>=la and ordi<lz :
            # r.join()
            r.append(chr(((ordi-la+13)%26)+la))
            #print r
        elif ordi>=ua and ordi<uz :
            # r.join()
            r.append(chr(((ordi-ua+13)%26)+ua))
        elif c =='&':
            r.append('&amp;')
        elif c =='<':
            r.append('&lt;')
        elif c =='>':
            r.append('&gt;')
        elif c =='"':
            r.append('&quot;')
        else:
            r.append(c)

    return ''.join(r)
