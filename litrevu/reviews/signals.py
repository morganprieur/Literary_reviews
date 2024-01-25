
# from reviews.models import (
#     Ticket, Review, UserFollows
# ) 
# from django.contrib.auth.hashers import make_password 
# from django.contrib.auth.models import User, Group 
# from django.db.models.signals import post_save, pre_save 
# from django.dispatch import receiver 
# from datetime import datetime 


# # Quand on crée une Review et que Ticket est vide : 
# #   un Ticket est créé, 
# # #   et le groupe "owner_group" est ajouté à ses groupes 
# @receiver(pre_save, sender=Review) 
# def create_ticket(sender, instance, **kwargs): 
#     """ When a Review instance is going to be created: 
#             creates a Ticket with title 'Ticket for ' + instance headline (?) 
#             # and assign the new User a 'owner_group'.  
#         Args: 
#             sender (Review): the model sends a signal when an instance is going to be created 
#             instance (Review): the going to be created Review 
#     """ 
#     # # Création d'un User, avec mot de pass hashé 
#     # Création d'un Ticket pour le User du request 
#     print('sender : ', sender) 
#     print('sender.headline : ', sender.headline) 
#     print('sender.user : ', sender.user) 
#     print('sender.user.get_queryset() : ', sender.user.get_queryset()) 
#     # print('dir(sender.user) : ', dir(sender.user)) 
#     print('instance : ', instance) 
#     # print('request : ', request) 
#     print('kwargs : ', kwargs) 
#     rev_user = User.objects.get(username='member_01') 
#     new_ticket = Ticket( 
#         title='Ticket for ' + str(sender.headline), user=rev_user) 
#     # if len(instance.password) < 20: 
#     #     new_user.password = make_password(instance.password) 
#     # else: 
#     #     # instance.password is already hashed: 
#     #     new_user.password = instance.password 
#     new_ticket.save() 

#     # Get the latest instance of created User: 
#     ticket = Ticket.objects.filter().last() 
#     print(ticket.title) 
    
#     # if user.username == 'cli_' + str(instance.name): 
#     #     # Adds the group 'owner_group' to the user's instance groups 
#     #     owner_group = Group.objects.get(name='owner_group') 
#     #     user.groups.add(owner_group) 
        
#     #     # Afficher la réussite de la création du User et la liste de ses groupes 
#     #     user_groups = user.groups.values_list('name', flat = True) 
#     #     groups_as_list = list(user_groups) 
#     #     print('User ' + str(user.username) + ' - groupes : ' + str(groups_as_list) + ' successfully saved!') 

# """ 
#     # # Quand on crée un Bei : 
#     # #   - un User est créé, 
#     # #   - le groupe "bei_group" est ajouté à ses groupes 
#     # @receiver(post_save, sender=Bei) 
#     # def create_bei_user(sender, instance, created, **kwargs): 
#     #     "" " When a Bei instance is created: 
#     #         creates a User with name 'bei_' + instance name 
#     #         and assign the new User a 'bei_group'.  
#     #         Args:
#     #             sender (Bei): the model sends a signal when an instance is created 
#     #             instance (Bei): the just created Bei 
#     #             created (bool): the Bei instance is created True/False : trigger. If False, the program exits the method.  
#     #     "" " 
#     #     if created: 
#     #         # Création d'un User, avec mot de pass hashé 
#     #         # User.objects.create(username='bei_' + str(instance), email='', password='pass_bei1') 
#     #         new_user = User( 
#     #             username='bei_' + str(instance.serial_number), 
#     #             email='' 
#     #         ) 
#     #         if len(instance.password) < 20: 
#     #             new_user.password = make_password(instance.password) 
#     #         else: 
#     #             # instance.password is already hashed 
#     #             new_user.password = instance.password  
#     #         new_user.save() 
            
#     #         # Get the latest instance of created User 
#     #         user = User.objects.filter().last() 
            
#     #         if user.username == 'bei_' + str(instance): 
#     #             # Adds the group 'bei_group' to the user's instance groups 
#     #             bei_group = Group.objects.get(name='bei_group') 
#     #             user.groups.add(bei_group) 
                
#     #             # Afficher la réussite de la création du User et la liste de ses groupes 
#     #             user_groups = user.groups.values_list('name', flat = True) 
#     #             groups_as_list = list(user_groups) 
#     #             print('User ' + str(user.username) + ' - groupes : ' + str(groups_as_list) + ' successfully saved!') 

            
#     #         if (Bei.objects.last() == str(instance)) and Installation.objects.last().bei == str(instance): 
#     #             last_bei=Bei.objects.last() 
#     #             last_installation = Installation.objects.last() 
#     #             # print(f'last_bei DSIG109 : {last_bei}') 
#     #             # print(f'last_installation DSIG110 : {last_installation}') 

#     #             new_maintenance = Maintenance( 
#     #                 bei=last_bei[0], 
#     #                 description = 'Installation', 
#     #                 maintenance_name = f'Installation {last_bei[0].serial_number}', 
#     #                 maintenance_date = last_installation.installation_date 
#     #             ) 
#     #             new_maintenance.save() 
#     #             print(f'new_maintenance DSIG115 : {Maintenance.objects.last()}') 


#     # # Quand un User est créé et que son nom commence par 'bei_' : 
#     # #   un Bei_profile est créé, qui lie le User et le Bei. 
#     # @receiver(post_save, sender=User) 
#     # def create_bei_profile(sender, instance, created, **kwargs): 
#     #     "" " When a User with name 'bei_'+ is created: 
#     #             creates a Bei_profile, in order to bind the User and the Client.   
#     #             Args:
#     #                 sender (User): the model sends a signal when an instance is created 
#     #                 instance (User): the just created User 
#     #                 created (bool): the User instance is created True/False: trigger. If False, the program exits the method.  
#     #     "" " 
#     #     bei = Bei.objects.filter().last() 
#     #     user = User.objects.filter(username__startswith='bei_').last() 
        
#     #     if created and user == instance: 
#     #         Bei_profile.objects.create(bei_user=instance, bei=bei) 
# """ 

