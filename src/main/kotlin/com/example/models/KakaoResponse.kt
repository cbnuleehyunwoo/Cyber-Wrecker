package com.example.models

import kotlinx.serialization.Serializable

@Serializable
data class KakaoRequest(
    val userRequest: UserRequest,
    val action: Action
)

@Serializable
data class UserRequest(
    val utterance: String
)

@Serializable
data class Action(
    val params: Map<String, String>
)

@Serializable
data class KakaoResponse(
    val version: String, // 기본값 제거하여 반드시 JSON에 포함되도록 함
    val template: KakaoTemplate
)

@Serializable
data class KakaoTemplate(
    val outputs: List<KakaoOutput>
)

@Serializable
data class KakaoOutput(
    // null인 경우 JSON에서 아예 제외되어야 함
    val listCard: KakaoListCard? = null,
    val simpleText: KakaoSimpleText? = null
)

@Serializable
data class KakaoSimpleText(
    val text: String
)

@Serializable
data class KakaoListCard(
    val header: KakaoHeader,
    val items: List<KakaoListItem>,
    val buttons: List<KakaoButton>? = null
)

@Serializable
data class KakaoHeader(
    val title: String
)

@Serializable
data class KakaoListItem(
    val title: String,
    val description: String? = null,
    val link: KakaoLink? = null
)

@Serializable
data class KakaoLink(
    val web: String
)

@Serializable
data class KakaoButton(
    val label: String,
    val action: String,
    val webLinkUrl: String? = null
)
