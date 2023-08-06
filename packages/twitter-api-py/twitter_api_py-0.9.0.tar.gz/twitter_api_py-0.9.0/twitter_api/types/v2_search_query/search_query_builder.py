from typing import Union

from typing_extensions import Any, Literal, overload

from twitter_api.types.v2_cashtag import Cashtag
from twitter_api.types.v2_dm_conversation.dm_conversation_id import DmConversationId
from twitter_api.types.v2_domain import DomainId
from twitter_api.types.v2_entity.entity_id import EntityId
from twitter_api.types.v2_entity.entity_name import EntityName
from twitter_api.types.v2_hashtag import Hashtag
from twitter_api.types.v2_language import Language
from twitter_api.types.v2_list.list_id import ListId
from twitter_api.types.v2_place.place_country_code import PlaceCountryCode
from twitter_api.types.v2_place.place_id import PlaceId
from twitter_api.types.v2_place.place_name import PlaceName
from twitter_api.types.v2_tweet.tweet_context_annotation import TweetContextAnnotation
from twitter_api.types.v2_tweet.tweet_id import TweetId
from twitter_api.types.v2_user.user_id import UserId
from twitter_api.types.v2_user.username import Username

from .operators.bounding_box_operator import BoundingBoxOperator
from .operators.cashtag_operator import CashtagOperator
from .operators.context_operator import ContextOperator
from .operators.conversation_id_operator import ConversationIdOperator
from .operators.entity_operator import EntityOperator
from .operators.from_user_operator import FromUserOperator
from .operators.group_operator import CompleteGroupOperator, IncompleteGroupOperator
from .operators.has_cashtags_operator import HasCashtagsOperator
from .operators.has_geo_operator import HasGeoOperator
from .operators.has_hashtags_operator import HasHashtagsOperator
from .operators.has_images_operator import HasImagesOperator
from .operators.has_links_operator import HasLinksOperator
from .operators.has_media_operator import HasMediaOperator
from .operators.has_mentions_operator import HasMentionsOperator
from .operators.has_video_link_operator import HasVideoLinkOperator
from .operators.hashtag_operator import HashtagOperator
from .operators.in_reply_to_tweet_id_operator import InReplyToTweetIdOperator
from .operators.is_nullcast_operator import IsNullcastOperator
from .operators.is_quote_operator import IsQuoteOperator
from .operators.is_reply_operator import IsReplyOperator
from .operators.is_retweet_operator import IsRetweetOperator
from .operators.is_verified_operator import IsVerifiedOperator
from .operators.keyword_operator import KeywordOperator
from .operators.lang_operator import LangOperator
from .operators.list_operator import ListOperator
from .operators.mention_operator import MentionOperator
from .operators.operator import CompleteOperator, IncompleteOperator
from .operators.place_country_operator import PlaceCountryOperator
from .operators.place_operator import PlaceOperator
from .operators.point_radius_operator import PointRadiusOperator
from .operators.quotes_of_tweet_id_operator import QuotesOfTweetIdOperator
from .operators.retweets_of_operator import RetweetsOfOperator
from .operators.retweets_of_tweet_id_operator import RetweetsOfTweetIdOperator
from .operators.to_user_operator import ToUserOperator
from .operators.url_operator import UrlOperator


class SearchQueryBuilder:
    @overload
    def group(self, operator: CompleteOperator) -> CompleteGroupOperator:
        ...

    @overload
    def group(self, operator: IncompleteOperator) -> IncompleteGroupOperator:
        ...

    def group(self, operator: Union[CompleteOperator, IncompleteOperator]):
        """
        括弧で囲みたい対象を指定する。括弧で囲まれた対象は優先的に計算される。

        要素数が 1 つの場合は括弧をつけない。
        """
        if isinstance(operator, CompleteOperator):
            return CompleteGroupOperator(operator)
        else:
            return IncompleteGroupOperator(operator)

    def keyword(self, keyword: str) -> KeywordOperator:
        """
        キーワードによる絞り込み。

        空白が含まれる場合、ダブルクォーテーションで囲まれる。
        """
        return KeywordOperator(keyword)

    def mention(self, username: Username) -> MentionOperator:
        """
        メンションによる絞り込み。

        先頭に @ がない場合、 @ をつけて処理される。
        """
        return MentionOperator(username)

    def hashtag(self, hashtag: Hashtag) -> HashtagOperator:
        """
        ハッシュタグによる絞り込み。

        先頭に # がない場合、 # をつけて処理される。
        """
        return HashtagOperator(hashtag)

    def cashtag(self, cashtag: Cashtag) -> CashtagOperator:
        """
        キャッシュタグによる絞り込み。

        先頭に $ がない場合、 $ をつけて処理される。
        """
        return CashtagOperator(cashtag)

    def from_user(self, user: Union[UserId, Username]) -> FromUserOperator:
        """
        どのユーザからツイートされたかで絞り込む。
        """
        return FromUserOperator(user)

    def to_user(self, user: Union[UserId, Username]) -> ToUserOperator:
        """
        どのユーザへツイートしたかで絞り込む。
        """
        return ToUserOperator(user)

    def url(self, url: str) -> UrlOperator:
        """
        ツイートに含まれる URL で絞り込む。
        """
        return UrlOperator(url)

    def retweets_of(self, user: Union[UserId, Username]) -> RetweetsOfOperator:
        """
        どのユーザへのリツイートかで絞り込む。
        """
        return RetweetsOfOperator(user)

    def in_reply_to_tweet_id(self, id: TweetId) -> InReplyToTweetIdOperator:
        """
        どのツイートへのリプライかで絞り込む。
        """
        return InReplyToTweetIdOperator(id)

    def retweets_of_tweet_id(self, id: TweetId) -> RetweetsOfTweetIdOperator:
        """
        どのツイートへのリツイートかで絞り込む。
        """
        return RetweetsOfTweetIdOperator(id)

    def quotes_of_tweet_id(self, id: TweetId) -> QuotesOfTweetIdOperator:
        """
        どのツイートへの引用ツイートかで絞り込む。
        """
        return QuotesOfTweetIdOperator(id)

    @overload
    def context(
        self,
        context: TweetContextAnnotation,
        *,
        domain_id: Literal[None] = None,
        entity_id: Literal[None] = None,
    ) -> ContextOperator:
        ...

    @overload
    def context(
        self,
        context: Literal[None] = None,
        *,
        domain_id: DomainId,
        entity_id: EntityId,
    ) -> ContextOperator:
        ...

    def context(
        self,
        context: Any = None,
        *,
        domain_id: Any = None,
        entity_id: Any = None,
    ) -> ContextOperator:
        """
        ツイートの持つコンテキスト情報による絞り込み。

        refer: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
        """
        return ContextOperator(
            context,
            domain_id=domain_id,
            entity_id=entity_id,
        )

    def entity(self, name: EntityName) -> EntityOperator:
        """
        エンティティによる絞り込み。

        refer: https://developer.twitter.com/en/docs/twitter-api/annotations/overview
        """
        return EntityOperator(name)

    def conversation_id(self, id: DmConversationId) -> ConversationIdOperator:
        """
        どの DM 会話でのツイートかで絞り込む。
        """
        return ConversationIdOperator(id)

    def list(self, id: ListId) -> ListOperator:
        """
        指定したリストに入っているユーザのツイートかで絞り込む。

        リストに関しては、下記のリンクを参照。

        refer: https://developer.twitter.com/en/docs/twitter-api/lists/list-lookup/api-reference
        refer: https://developer.twitter.com/en/docs/twitter-api/lists/manage-lists/api-reference
        """
        return ListOperator(id)

    def place(self, place: Union[PlaceId, PlaceName]) -> PlaceOperator:
        """
        どの場所でのツイートかで絞り込む。
        """
        return PlaceOperator(place)

    def place_country(self, code: PlaceCountryCode) -> PlaceCountryOperator:
        """
        どの国からのツイートかで絞り込む。
        """
        return PlaceCountryOperator(code)

    @overload
    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: int,
        radius_mi: Literal[None] = None,
    ) -> PointRadiusOperator:
        ...

    @overload
    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Literal[None] = None,
        radius_mi: int,
    ) -> PointRadiusOperator:
        ...

    def point_radius(
        self,
        *,
        longitude_deg: float,
        latitude_deg: float,
        radius_km: Any = None,
        radius_mi: Any = None,
    ) -> PointRadiusOperator:
        """
        どの位置座標からのツイートかで絞り込む。

        - `longitude` の範囲： ±180[deg]
        - `latitude` の範囲： ±90[deg]
        - `radius` の最大値： 40[km] ≒ 25[mi]
        """
        return PointRadiusOperator(
            longitude_deg=longitude_deg,
            latitude_deg=latitude_deg,
            radius_km=radius_km,
            radius_mi=radius_mi,
        )

    def bounding_box(
        self,
        *,
        west_longitude_deg: float,
        south_latitude_deg: float,
        east_longitude_deg: float,
        north_latitude_deg: float,
    ) -> BoundingBoxOperator:
        """
        どの地図範囲からのツイートかで絞り込む。

        - `longitude` の範囲： ±180[deg]
        - `latitude` の範囲： ±90[deg]
        """
        return BoundingBoxOperator(
            west_longitude_deg=west_longitude_deg,
            south_latitude_deg=south_latitude_deg,
            east_longitude_deg=east_longitude_deg,
            north_latitude_deg=north_latitude_deg,
        )

    def is_retweet(self) -> IsRetweetOperator:
        """
        リツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsRetweetOperator()

    def is_reply(self) -> IsReplyOperator:
        """
        返信ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsReplyOperator()

    def is_quote(self) -> IsQuoteOperator:
        """
        引用ツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsQuoteOperator()

    def is_verified(self) -> IsVerifiedOperator:
        """
        認証ユーザのツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsVerifiedOperator()

    def is_nullcast(self) -> IsNullcastOperator:
        """
        Nullcast であるかどうかの絞り込み。

        否定形としてしか使えないことに注意。
        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return IsNullcastOperator()

    def has_hashtags(self) -> HasHashtagsOperator:
        """
        ハッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasHashtagsOperator()

    def has_cashtags(self) -> HasCashtagsOperator:
        """
        キャッシュタグのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasCashtagsOperator()

    def has_links(self) -> HasLinksOperator:
        """
        リンクのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasLinksOperator()

    def has_mentions(self) -> HasMentionsOperator:
        """
        メンションのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasMentionsOperator()

    def has_media(self) -> HasMediaOperator:
        """
        メディアのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasMediaOperator()

    def has_images(self) -> HasImagesOperator:
        """
        画像のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasImagesOperator()

    def has_video_link(self) -> HasVideoLinkOperator:
        """
        ビデオのついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasVideoLinkOperator()

    def has_geo(self) -> HasGeoOperator:
        """
        位置情報のついたツイートであるかどうかの絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return HasGeoOperator()

    def lang(self, lang: Language) -> LangOperator:
        """
        言語による絞り込み。

        単体では成立しないため、成立する他のクエリと AND 結合する必要がある。
        """
        return LangOperator(lang)
