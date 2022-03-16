from django.views               import View
from django.http                import JsonResponse
from django.db.models           import Q, Avg, IntegerField
from django.db.models.functions import Cast
from django.db                  import connection

from time                       import strftime
import random
import datetime
from datetime import date
import pandas as pd

from insight.models             import InfluencerPost, Insight

class SearchView(View):
    def get(self, request):
        try:
            contract    = request.GET.get('contract', None)
            influencers = request.GET.get('influencer', None)
            weeks       = request.GET.get('weeks')

            now = datetime.datetime.utcnow()

            q = Q()

            '''
            현재 다른 태그는 campaign__end_at 에 
            들어가있지않아서
            검색이 되지않음
            '''
            if contract == 'in_progress':
                q &= Q(campaign__end_at__gt = now)

            if contract == 'complete':
                q &= Q(campaign__end_at__lt = now)
            
            if influencers:
                q &= Q(influencer__full_name = influencers)

            if weeks == '1':
                q &= Q(insight__created_at__range=('2022-01-15', '2022-03-08'))

            if weeks == '2':
                q &= Q(insight__created_at__range=('2022-03-08', '2022-03-15'))

            if weeks == '3':
                q &= Q(insight__created_at__range=('2022-03-15', '2022-03-22'))

            if weeks == '4':
                q &= Q(insight__created_at__range=('2022-03-22', '2022-03-31'))

            if weeks == 'all':
                q &= Q(insight__created_at__range=('2022-01-01', '2022-03-31'))

            influencers = InfluencerPost.objects.filter(q, tag__in=['@discoveryexpedition_kr']).distinct('influencer__full_name')
            random_data = random.randint(300, 1000)

            total_report = [{
                'full_name'                : influencer.influencer.full_name,
                'profile_image'            : influencer.influencer.profile_image,
                #'end_date'                 : influencer.campaign.end_at.strftime('%Y-%m-%d'),
                #'campaign'                 : influencer.campaign.name,
                #'contract'                 : influencer.campaign.contract,
                # # account_value 작업 필요함
                # 'account_value'          : influencer.insight_set.aggregate(value = Cast(Avg('male_follower') + Avg('female_follower'),output_field = IntegerField()))['value'],
                'age'                      : influencer.influencer.age,
                'live'                     : influencer.influencer.live,
                'follower'                 : influencer.insight_set.aggregate(value = Avg('male_follower') + Avg('female_follower'))['value'],
                'like'                     : influencer.insight_set.aggregate(value = Cast(Avg('like'), output_field = IntegerField()))['value'],
                'comment'                  : influencer.insight_set.aggregate(value = Cast(Avg('comment'), output_field = IntegerField()))['value'],
                'hashtag'                  : influencer.insight_set.aggregate(value = Cast(Avg('hashtag'), output_field = IntegerField()))['value'],
                'exposure'                 : influencer.insight_set.aggregate(value = Cast(Avg('exposure'), output_field = IntegerField()))['value'],
                'discover'                 : influencer.insight_set.aggregate(value = Cast((Avg('exposure') - random_data),output_field = IntegerField()))['value'],
                'participation'            : influencer.insight_set.aggregate(value = Cast(Avg('exposure') - (Avg('exposure') - random_data), output_field = IntegerField()))['value'],
                'participation_percentage' : influencer.insight_set.aggregate(value = Cast((Avg('exposure') - random_data) * 100 / Avg('exposure'), output_field = IntegerField()))['value'],
                'tag'                      : influencer.tag,
                'like'                     : influencer.insight_set.aggregate(value = Cast(Avg('like'), output_field = IntegerField()))['value'],
                'comment'                  : influencer.insight_set.aggregate(value = Cast(Avg('comment'), output_field = IntegerField()))['value']
            }for influencer in influencers]

            hashtag_compare = InfluencerPost.objects.filter(q).exclude(tag__in=['@discoveryexpedition_kr']).distinct('tag')
            influencer_hashtag_performence = [{
                'NAME' : compares.influencer.full_name,
                'tag' : compares.tag,
                'like' : compares.insight_set.aggregate(value = Cast(Avg('like'), output_field = IntegerField()))['value'],
                'comment' : compares.insight_set.aggregate(value = Cast(Avg('comment'), output_field = IntegerField()))['value'],
            }for compares in hashtag_compare]

            influencer_hashtag_inflow = [{
                'NAME' : compares.influencer.full_name,
                'tag' : compares.tag,
                'exposure' : compares.insight_set.aggregate(value = Cast(Avg('exposure'), output_field = IntegerField()))['value'],
                'hashtag' : compares.insight_set.aggregate(value = Cast(Avg('hashtag'), output_field = IntegerField()))['value'],
            }for compares in hashtag_compare]

            '''
            공식 계정이 아닌 타 태그들은
            공식태그인 #discoveryexpedition_kr 보다
            낮게 해야합니다.
            '''
            reaction_conversion = [{
                'NAME' : compares.influencer.full_name,
                'tag' : compares.tag,
                '반응(인스타 공식 계정방문을 반응으로 함)' : compares.insight_set.aggregate(value = Cast(Avg('official_visit'), output_field = IntegerField()))['value'],
                '전환률(인스타에서 공식 홈페이지로)' : compares.insight_set.aggregate(value = Cast(Avg('official_referrer'), output_field = IntegerField()))['value'],
            }for compares in hashtag_compare]

            participation = [{
                'NAME' : compares.influencer.full_name,
                'tag' : compares.tag,
                'participation'            : compares.insight_set.aggregate(value = Cast(Avg('exposure') - (Avg('exposure') - random_data), output_field = IntegerField()))['value'],
                'participation_percentage' : compares.insight_set.aggregate(value = Cast((Avg('exposure') - random_data) * 100 / Avg('exposure'), output_field = IntegerField()))['value'],
            }for compares in hashtag_compare]

            '''
            Q 객체로 분리해줘야합니다.
            '''
            insight = InfluencerPost.objects.filter(tag__in=['@discoveryexpedition_kr']).distinct('influencer__full_name')
            influencer_performance_top3 = [{
                'name' : insights.influencer.full_name,
                'tag' : insights.tag,
                'participation_percentage' : insights.insight_set.aggregate(value = Cast((Avg('exposure') - random_data) * 100 / Avg('exposure'), output_field = IntegerField()))['value'],
            }for insights in insight]

            
            # past = InfluencerPost.objects.filter(q, campaign__end_at__lte = datetime.timedelta(days= -60))
            # past_data = [{
            #     'test' : past_datas.campaign.name
            # }for past_datas in past]

            gender_compare = [{
                'male'   : influencer.insight_set.aggregate(value = Cast(Avg('male_follower'), output_field = IntegerField()))['value'],
                'female' : influencer.insight_set.aggregate(value = Cast(Avg('female_follower'), output_field = IntegerField()))['value']
            }for influencer in influencers]

            gd_frame = pd.DataFrame(gender_compare)
            
            male   = gd_frame['male'].mean().round(1)
            female = gd_frame['female'].mean().round(1)

            '''
            소숫점 한자리 까지 표현해야함
            '''
            gender_compare = {
                'male'              : male,
                'female'            : female,
                'male_percentage'   : int(male / (male + female) * 100),
                'female_percentage' : int(female / (male + female) * 100)
            }

            result = {
                'total_result'   : total_report,
                'influencer_hashtag_performence' : influencer_hashtag_performence ,
                'influencer_hashtag_inflow' : influencer_hashtag_inflow,
                'reaction_conversion' : reaction_conversion,
                'participation' : participation,
                'top3_influencers' : (sorted(influencer_performance_top3, key = lambda i: i['participation_percentage'],reverse=True))[:3],
                'gender_compare' : gender_compare,
            }
            #print(connection.queries)
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR : NO_DATA'}, status = 400)