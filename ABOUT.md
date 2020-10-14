# Purpose of the App
During mass protests in Belarus 2020, hundres of people are arrested each week. Relatives, friends might have struggle to find information about arrested person, because there are multiple official sources, which might be unavailable at the moment, and also number of unoficcial sources, which are spreaded across several web-sites and telegram channels. SpiskiApp was created to help anyone to quickly find information about arrested person. And, from the other hand. help volunteers manage lists of arrestants. It should offload volunteers and let them focus on more mportant things.

Ultimately, we are answering this question: **Where is a person?**

# Users of the App
There are two kinds of users:
* User - An anonymous person who might search information about an arrested person.
* Volunteer - An authorized person, which could add information about arrested persons.
* Admin - could invite and manage Volunteers
* (Superuser) - technical role, representing core team of the project. From workflow perspective - could manage Admins.

## User
User workflow is straightforward - by using a client-app (TBD. web-site, mobile app, tg. bot), user provides something of first/last name and birth date and gets response from the App. The response contains list of all arrestant's status changes. The user sees at which police post / prison holds the arrestant. Might also see some optional info regarding court, incriminated chapter, detention details etc.

## Volunteer
This role is privileged and load lists or change arrestant's status (Lists usually published at Okrestina Spiski th. channel). To became a volunteer you have to be invited by an Admin. This role required to be logged in.

## Admin
Is basically a Volunteer, which could manage other volunteers (without ability to grant/revoke Admin role).

# Detention process
TODO

# Entity Relation
TODO

# Release plan and our priorities
Goals:
* Release
* Implementing core workflows
* Integration with Vesna/Hapun/OkrestinaSpiski/SpiskiBot

Not goals:
* Client apps (we going to have something basic, though)
* Automated data infill (We have enough volunteers, who could help with that)

# Ethical notes
By request of the relative or the person, we will hide all information about detention.
