from django.db import models

class Company(models.Model):
    name       = models.CharField(max_length = 50)
    created_at = models.DateTimeField(null = True)
    updated_at = models.DateTimeField(null = True)

    class Meta:
        db_table = 'companies'

class Performance(models.Model):
    sale       = models.IntegerField()
    company    = models.ForeignKey(Company, on_delete = models.CASCADE)
    created_at = models.DateTimeField(null = True)

    class Meta:
        db_table = 'performances'

class Influencer(models.Model):
    name          = models.CharField(max_length = 50)
    full_name     = models.CharField(max_length = 15)
    age           = models.IntegerField()
    live          = models.CharField(max_length = 15)
    profile_image = models.URLField(max_length = 250)
    company       = models.ForeignKey(Company, on_delete = models.CASCADE)
    created_at    = models.DateTimeField(null = True)
    updated_at    = models.DateTimeField(null = True)

    class Meta:
        db_table = 'influencers'

class Campaign(models.Model):
    name        = models.CharField(max_length = 50)
    tag         = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    image       = models.URLField(max_length = 250)
    contract    = models.BooleanField()
    budget      = models.IntegerField()
    created_at  = models.DateTimeField(null = True)
    updated_at  = models.DateTimeField(null = True)
    end_at      = models.DateTimeField(null = True)

    class Meta:
        db_table = 'campaigns'

class InfluencerPost(models.Model):
    tag           = models.CharField(max_length = 100)
    url           = models.URLField(max_length = 250)
    created_at    = models.DateTimeField(null = True)
    campaign      = models.ForeignKey(Campaign, null = True, on_delete = models.CASCADE)
    influencer    = models.ForeignKey(Influencer, on_delete = models.CASCADE)

    class Meta:
        db_table = 'influencer_posts'

class Insight(models.Model):
    search_frequency   = models.IntegerField()
    visit_frequency    = models.IntegerField()
    like               = models.IntegerField()
    comment            = models.IntegerField()
    male_follower      = models.IntegerField()
    female_follower    = models.IntegerField()
    bookmark           = models.IntegerField()
    exposure           = models.IntegerField()
    profile            = models.IntegerField()
    profile_visit      = models.IntegerField()
    website_click      = models.IntegerField()
    hashtag            = models.IntegerField()
    reaction           = models.IntegerField()
    home               = models.IntegerField()
    official_visit     = models.IntegerField()
    official_follower  = models.IntegerField()
    official_referrer  = models.IntegerField()
    influencer         = models.ForeignKey(Influencer, on_delete = models.CASCADE)
    influencer_post    = models.ForeignKey(InfluencerPost, on_delete = models.CASCADE)
    created_at         = models.DateTimeField(null = True)

    class Meta:
        db_table = 'insights'

class SocialNetworkService(models.Model):
    name       = models.CharField(max_length = 50)
    created_at = models.DateTimeField(null = True)
    updated_at = models.DateTimeField(null = True)

    class Meta:
        db_table = 'social_network_services'

class Snsinfo(models.Model):
    post                      = models.IntegerField()
    url                       = models.URLField(max_length = 250)
    social_network_service    = models.ForeignKey(SocialNetworkService, on_delete = models.CASCADE)
    influencer                = models.ForeignKey(Influencer, on_delete = models.CASCADE)
    created_at                = models.DateTimeField(null = True)

    class Meta:
        db_table = 'sns_infos'