class Approuter: 
   def db_for_read(self,model,**hints):
      if(model._meta.app_label == 'scrape'):
         return "default"
      elif(model._meta.app_label == 'DB'):
         return 'postgres'
      return None
   def db_for_write(self,model,**hints):
        if(model._meta.app_label == 'scrape'):
         return "default"
        elif(model._meta.app_label == 'DB'):
         return 'postgres'
        return None
   def db_for_migrations(self,db,app_label,model_name = None,**hints):
      if(app_label=='scrape'):
         return db=='default'
      elif(app_label == 'DB'):
         return db=='postgres'
      return None
