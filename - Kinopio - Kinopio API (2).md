---
source: "https://kinopio.club/help/api"
author:
published:
created: 2026-04-19
---
![](https://kinopio.club/help/assets/cat.png)

The Kinopio API is used to find, save, and update the spaces of signed up users. You can use it to make cool things too.

Use of the API is subject to the [Use Restrictions Policy](https://kinopio.club/help/posts/use-restrictions-policy/).

## Authentication

Kinopio uses token-based authentication using your user `apiKey`. You can get your apiKey in the app through `User → Settings → Account → API`.

> 🙈 Your API key carries the same privileges as your user account, so be sure to keep it secret!

Use your apiKey in the `Authorization` header of each request.

(For testing, you can also use a query string (`?apiKey=`) but this is less secure and not recommended)

## Rate Limits

The API is limited to 5 requests per second. If you exceed this rate, you will receive a `429` response and will need to wait 30 seconds before subsequent requests will succeed.

## Routes

## All

[https://api.kinopio.club](https://api.kinopio.club/) is the base path for all routes

| Method | Name | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/` | Confirm that the API server is online | None |

## Users

Users are representations of any account on Kinopio. Users are created by the server when they sign up.

### User Routes

Routes with Auth as `apiKey` mean that the Authorization header apiKey must match the requested user.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/user/public/:userId` | Gets public info on a user | None |
| `GET` | `/user/public/explore-spaces/:userId` | The a list of spaces with `showInExplore: true` created by the user | None |
| `GET` | `/user/hidden-spaces` | Get hidden spaces for the authenticating user | `apiKey` |
| `GET` | `/user/public/multiple?userIds=id1,id2` | Gets public info for multiple userIds, up to 60 userIds at a time | None |
| `GET` | `/user` | Get all info on the authenticating user | `apiKey` |
| `GET` | `/user/favorite-spaces` | Get favorite spaces for the authenticating user. Favorited spaces which have unread updates will have `isEdited: true` | `apiKey` |
| `GET` | `/user/favorite-users` | Get favorite users for the authenticating user | `apiKey` |
| `GET` | `/user/favorite-colors` | Get favorite colors for the authenticating user | `apiKey` |
| `GET` | `/user/spaces` | Get a list of the user's [Spaces](#spaces). Use `/user/group-spaces` for spaces created by other members of groups they belong to | `apiKey` |
| `GET` | `/user/groups` | Get a list of the user's groups. Their role in each group (`member` or `admin`) is inside the `groupUser` object | `apiKey` |
| `GET` | `/user/group-spaces` | Get a list of the user's group [Spaces](#spaces) created by other members of groups they belong to | `apiKey` |
| `GET` | `/user/template-spaces` | Get a list of the user's template [Spaces](#spaces). These include template spaces you made or are a collaborator in | `apiKey` |
| `GET` | `/user/removed-spaces` | Get [Spaces](#spaces) removed by the authenticating user | `apiKey` |
| `GET` | `/user/inbox-space` | Get info on the user's `Inbox` space. whether a space is an inbox or not is based on name only, so it's possible to have multiple `Inbox` spaces, but only one the most recently updated Inbox will be returned | `apiKey` |
| `GET` | `/user/tags` | Get a list of the last edited in your spaces | `apiKey` |
| `GET` | `/user/todos` | Get todo cards and boxes (item names start with `[]`, `[ ]`, or `[x]`), grouped by space | `apiKey` |
| `PATCH` | `/user` | Update the authenticating user(s) based on an object body with user attributes. You can't patch `apiKey`, `password`, `emailIsVerified`, or `email` | `apiKey` |

### User Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the user. Is not user updateable |
| `apiKey` | `UUID` | Used in Authentication headers to make API calls as the currentUser. Generated and returned only when user signs up or in. Is not user updateable |
| `cardsCreatedCount` | `Integer` | The number of cards the user has created if they're not a paid user, used to enforce the free user limit. Is not user updatable. |
| `cardsCreatedCountRaw` | `Integer` | Similar to `cardsCreatedCount` except the raw version increments even if your're a free user on a paid user space. This is a vanity metric and is not used to enforce free user limits. |
| `cardSettingsDefaultCharacterLimit` | `Integer` | The max number of characters you can enter in a card. Either 300 (default) or 4000 (max). Constrained character limits are meant to encourage using cards to represent single ideas. But this override exists for those who don't want that. |
| `cardSettingsCardWrapWidth` | `Integer` | Sets the maximum default length of a card before it starts wrapping on cards created by the user |
| `cardSettingsShiftEnterShouldAddChildCard` | `Boolean` | Sets whether shift-enter while editing a card creates a new-child (`true`) or a line break (`false`) |
| `color` | `String` | User color changes your paint stroke and default avatar color |
| `createdAt` | `String` | The date when the user was created |
| `creditsEarned` | `Integer` | The number of $ credits earned by referring or inviting new users to Kinopio. Is not user updateable |
| `creditsUsed` | `Integer` | The number of $ credits subtracted from your payments so far. Is not user updateable |
| `defaultCardBackgroundColor` | `String` | User preference for a default background color to use for new cards |
| `defaultSpaceBackground` | `String` | User preference for a default background url to use for new spaces. This becomes `null` if `defaultSpaceBackgroundGradient` is set. |
| `defaultSpaceBackgroundGradient` | `Object` | User preference for the default background gradient to use for new spaces. This becomes `null` if `defaultSpaceBackground` is set. |
| `defaultSpaceBackgroundTint` | `String` | User preference for a default background color used to tint new spaces |
| `defaultConnectionControlPoint` | `String` | User preference for the default control point for new connections. `null` makes a curved path, `q00,00` makes a straight line |
| `description` | `String` | A description of this particular user |
| `email` | `String` | The unique email address of the user required to create an account |
| `emailIsVerified` | `Boolean` | Whether the user has verified their email address |
| `filterShowAbsoluteDates` | `Boolean` | Whether card dates are displayed as absolute (false is default relative) |
| `filterComments` | `Boolean` | Whether comment cards are hidden to the user |
| `filterShowDateUpdated` | `Boolean` | Whether the user has has toggled the card date filter |
| `filterShowUsers` | `Boolean` | Whether the user has has toggled the card user filter |
| `isAmbassador` | `Boolean` | Whether the user is in the [friends of kinopio](https://kinopio.club/friends-of-kinopio-ambassadors-YNmS6C3fofN3R9mYgO1Bu) ambassador program. Is not user updatable. |
| `isDonor` | `Boolean` | Whether the user has donated to Kinopio. Is not user updatable. |
| `isModerator` | `Boolean` | Whether the user is a moderator of the community forums or discord. Is not user updatable. |
| `isDebugMode` | `Boolean` | Whether the user has debug mode enabled, which displays item ids and other attributes in the kinopio-client. |
| `isUpgraded` | `Boolean` | Whether the user currently has a paid subscription. Is not user updatable. |
| `lastReadNewStuffId` | `String` | The id of the last read article from the 'new stuff' newsfeed |
| `lastUsedImagePickerService` | `String` | The user's last used image picker service, is either `stickers`, `gifs`, `bing`, `backgrounds`, `recent`, `ai` |
| `lastSidebarSection` | `String` | The shortname of the sidebar section last viewed. Can be `stats`, `inbox`, `removed`, `links`, `favorites`, `history`, `minimap`, `tags`, `todos`, `note`. Defaults to `inbox`. |
| `lastSpaceId` | `String` | The spaceId of the last space edited. Used to return you to the same space the next time you visit kinopio.club |
| `name` | `String` | The unique name of the user. Is a url-safe string (no spaces or special characters) because it's also used for url slugs |
| `prevHeaderFontId` | `Integer` | The id of the previous header font selected. Default value is `0` for Recoleta |
| `prevInviteEmails` | `String` | The emails you last used when emailing space invites. Is private user info. |
| `shouldEmailBulletin` | `Boolean` | Whether the user has chosen to allow bulletin emails (default to true) |
| `shouldEmailNotifications` | `Boolean` | Whether the user has chosen to allow notification emails (default to true) |
| `shouldEmailWeeklyReview` | `Boolean` | Whether the user has chosen to allow weekly review emails (default to true) |
| `shouldIncreaseUIContrast` | `Boolean` | User preference for whether the header and footer buttons should not be translucent or transparent in any way |
| `shouldUseLastConnectionType` | `Boolean` | Whether the user has chosen to use last connection type for new connections (default to true) |
| `shouldShowMoreAlignOptions` | `Boolean` | Whether the user has chosen to view more card position alignment and distribution options (default to true) |
| `shouldShowCurrentSpaceTags` | `Boolean` | Whether the user has chosen should only tags in the current space in the Tags dialog |
| `shouldShowItemActions` | `Boolean` | Whether extra card formatting options (h1, h2, etc.) buttons are visible in the card details dialog |
| `shouldShowMultipleSelectedBoxActions` | `Boolean` | Whether extra box formatting options (color, fill, etc.) buttons are visible in the multiple selected items dialog |
| `shouldShowMultipleSelectedLineActions` | `Boolean` | Whether extra connection formatting options (type, reverse, etc.) buttons are visible in the multiple selected items dialog |
| `shouldShowMultipleSelectedListActions` | `Boolean` | Whether extra list formatting options (color, etc.) buttons are visible in the multiple selected items dialog |
| `shouldNotifyUnlockedStickyCards` | `Boolean` | Whether to eventually notify users that they've unlocked sticky cards (true for new users only, triggered after they create 20 cards) |
| `shouldPauseConnectionDirections` | `Boolean` | User pereference for whether connection directions should be static, instead of animating along their connection path |
| `shouldUseStickyCards` | `Boolean` | User pereference for whether cards should stick to their mouse cursor |
| `shouldShowMinimapJumpToList` | `Boolean` | Whether the list of boxes to jump to is expanded in the Minimap dialog |
| `showInExploreUpdatedAt` | `String` | When the user last opened the Explore dialog. Used to determine new/unread Explore spaces |
| `showItemActions` | `Boolean` | Whether the user has chosen to show expanded options and info in both the `card-details` and `multiple-selected-actions` dialogs |
| `sidebarResizeWidth` | `Integer` | Manually resized width of the sidebar dialog |
| `groups` | `JSON Array` | The groups a user belongs to, including public metadata on the other `users` in each group |
| `updatedAt` | `String` | The date when any changes to the user was made. Also is updated whenever the user starts a Kinopio session |
| `website` | `String` | The user's website, url validity is not checked |
| `prevSettingsSection` | `String` | The last used settings section. Can be `general`, `controls`, or `cards` |
| `outsideSpaceBackgroundIsStatic` | `Boolean` | User preference for whether the outside space area should use dynamically cycling colors, or whether it should be static grey |
| `studentDiscountIsAvailable` | `Boolean` | Whether the user is eligible for a student discount. Is not user updateable |
| `shouldShowMinimap` | `Boolean` | Whether the bottom-right minimap is persistently visible |

## Spaces

Spaces are where your [Cards](#cards) and [Connections](#connections) live.

### Space Routes

Routes with Auth `canViewSpace` or `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to view or edit the space.

The `closed` privacy state refers to `Public Read Only`.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/space/:spaceId` | Get info on a space by id. Use `?textOnly=true` for card names only | `canViewSpace` |
| `GET` | `/space/:spaceId/public-meta` | Get public space info on non-private spaces | None |
| `GET` | `/space/:spaceId/favorites` | Get a list of users who have favorited the spaceId | None |
| `GET` | `/space/:spaceId/feed.json` | `RSS feed` for cards recently created or updated in a space. Use `?apiKey=` for private spaces | `canViewSpace` |
| `GET` | `/space/:spaceId/   removedCards` | Get [Cards](#cards) removed in a space | `canEditSpace` |
| `GET` | `/space/explore-spaces` | Get a list of recently updated public spaces which have been added to Explore. Sorted by date `showInExploreUpdatedAt` | None |
| `GET` | `/space/explore-spaces/feed.json` | `RSS feed` for new spaces added to Explore | None |
| `GET` | `/space/live-spaces` | Get a list of currently being edited spaces which are open or closed | None |
| `GET` | `/space/multiple?spaceIds=id1,id2` | Get info on multiple spaces, up to 60 spaceIds at a time | `canViewSpace` |
| `GET` | `/space/public/multiple?spaceIds=id1,id2` | Gets public info for multiple public spaces, up to 60 spaceIds at a time. None |  |
| `GET` | `/space/inbox` | Get the current user's inbox space | `apiKey` |
| `GET` | `/space/everyones-spaces` | Get a list of recent public spaces sorted by date `createdAt` | None |
| `GET` | `/space/everyones-spaces/feed.json` | `RSS feed` for recent public spaces | None |
| `GET` | `/space/date-image` | Get the image url for today's date card image | None |
| `POST` | `/space` | Create a new space(s) from object(s) in request body. The owner will be the apiKey user | `apiKey` |
| `POST` | `/space/search-explore-space` | Get all `showInExplore` spaces based on space name. Body object must contain `query`. Searches are not case-insensitive | None |
| `PATCH` | `/space` | Update space(s) from object(s) in request body | `canEditSpace` |
| `PATCH` | `/space/restore` | Restore removed space(s) from object(s) in request body | `canEditSpace` |
| `DELETE` | `/space` | Remove space(s) specified in request body | `canEditSpace` |
| `DELETE` | `/space/permanent` | Permanently remove space(s) specified in request body | `canEditSpace` |
| `DELETE` | `/space/collaborator` | Removes collaborator user from space. Request Body Keys: `spaceId`, `userId` | `canEditSpace` |

### Space Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the space. Is not user updateable |
| `background` | `String` | The image url used by the space background |
| `backgroundIsGradient` | `Boolean` | Whether the space background uses `backgroundGradient` (instead of the default `background`) |
| `backgroundGradient` | `Object` | An array of gradient layer data that's used to build the space background gradient. The gradients are layered and animated using the technique described by [Shelby Wilson](https://shelby.cool/#/gradients) |
| `backgroundTint` | `String` | The background color used to tint the space background |
| `boxes` | `Array` | A list of [Boxes](#boxes) in the space |
| `cards` | `Array` | A list of [Cards](#cards) in the space |
| `collaboratorKey` | `String` | Used like an apikey to allow editing, but just for that space. allows anonymous users who aren't signed in to edit a space. You can rotate this key, but you should still treat it as a secret |
| `collaborators` | `Array` | A list of users that can also edit the space |
| `connectionTypes` | `Array` | A list of [Connection Types](#connection-types) |
| `connections` | `Array` | A list of [Connections](#connections) |
| `createdAt` | `String` | The date when the space was created |
| `drawingImage` | `String` | The image url for drawings on the space. The image is regenerated on the server after each drawing stroke. |
| `editedAt` | `String` | The date when card contents in the space was last added or changed |
| `editedByUserId` | `String` | The user id of the last user who edited or created a card in the space |
| `isFromTweet` | `Boolean` | Whether the space was created by replying to a tweet with `@kinopioclub save` |
| `isHidden` | `Boolean` | Whether the space is hidden by the current user |
| `isFavorite` | `Boolean` | Whether the space is favorited by the current user |
| `isRemoved` | `Boolean` | Whether the space has been soft-removed. (can then be restored or permanently removed) |
| `isRestrictedByModerator` | `Boolean` | Whether the space has been marked as restricted. Restricted spaces are not shown in Explore, Live, or in the Everyone feed. This value cannot be patched, it is set manually by a moderator only when necessary. |
| `isTemplate` | `Boolean` | Whether the space is a [personal template](https://kinopio.club/help/posts/templates/) |
| `lines` | `Array` | A list of the Line dividers in the space |
| `lists` | `Object` | A list of the [Lists](#lists) in the space |
| `moonPhase` | `String` | Name of the moonPhase icon representing when the space was created. Possible values are `new-moon`, `waxing-crescent`, `waxing-quarter`, `waxing-gibbous`, `full-moon`, `waning-gibbous`, `waning-quarter`, `waning-crescent` |
| `name` | `String` | The name of the space |
| `note` | `String` | The sidebar space note associated with the current user |
| `ownerUserId` | `String` | The userId of the user who created the space. Used to create url slugs |
| `originSpaceId` | `String` | If the space was created by duplicating another space, the origin space id is recorded |
| `privacy` | `String` | Can be `open`, `closed`, `private` |
| `removedByUserId` | `String` | The user who soft-removed the space. All space users can restore it via the API, but only the user who removed it will see it listed |
| `previewImage` | `String` | URL for the large-sized preview jpg image associated with the space |
| `previewThumbnailImage` | `String` | URL for the thumbnail-sized preview jpg image associated with the space |
| `previewImagePrivate` | `String` | Same as `previewImage`, except images in cards are not rendered. This is used for private space unfurling. |
| `previewThumbnailImagePrivate` | `String` | Same as `previewImageThumbnail`, except images in cards are not rendered. This is used for private space unfurling. |
| `url` | `String` | The url of a space is determined by its `name` and `id`. For example, `kinopio.club/:space-name-:id` |
| `users` | `Array` | The user who created/owns the space (a space will always have only one user) |
| `showInExplore` | `Boolean` | Whether the space is shown in explore |
| `tags` | `Array` | A list of |
| `group` | `Object` | Information on the group that a space belongs to (if any), including public metadata on the other group `users` |
| `groupId` | `String` | The group id that the space belongs to. A space can only belong to one group. |
| `addedTogroupByUserId` | `String` | The user who added the space to the group |
| `updatedAt` | `String` | The date when any changes in the space were made including a member visiting it |
| `visits` | `Integer` | The number of times the space has been loaded by a person |
| `readOnlyKey` | `String` | Similar to `collaboratorKey` but only allows users and non-signed-in users to read a private space |

## Cards

Cards are the building blocks of [Spaces](#spaces). They have `x`, `y`, and `z` positions and a `name`.

### Cards Routes

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the card belongs to.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/card/:cardId` | Get info on a card | `canViewSpace` |
| `GET` | `/card/multiple?cardIds=id1,id2` | Get info on multiple cards, up to 60 cardIds at a time | `canViewSpace` |
| `GET` | `/card/by-tag-name/:tagName` | Get all cards with tag matching tagName in your [Spaces](#spaces) | `apiKey` |
| `GET` | `/card/by-link-to-space/:spaceId` | Get the cards and [Spaces](#spaces) where `linkToSpaceId` is `spaceId`. Will only return spaces that the user can view | `apiKey and canViewSpace` |
| `POST` | `/card/search` | Get all cards that match a query. Body object must contain `query`. Only matches cards created by the user. Does not return removed cards, or cards from removed spaces. Searches are not case-insensitive | `apiKey` |
| `POST` | `/card` | Create card from object in request body. Body object must contain `spaceId` and `name`. If not included, `x`, `y`, `z` will be positioned near the top left of the space, in a cascade pattern to prevent overlaps | `canEditSpace` |
| `POST` | `/card/to-inbox` | Create card saved to the user's `Inbox` space from object in request body and. Body object must contain `name`. Will return `404` if the user does not already have an `Inbox` space. Positioning works just like `POST /card` | `canEditSpace` |
| `POST` | `/card/multiple` | Creates multiple cards from an array of objects in request body. Works just like `POST /card` | `canEditSpace` |
| `POST` | `/card/list` | Add card to a [List](#lists) specified in request body. Body object must contain card `id`, and `listId`. If body object has `shouldPrepend: true`, the card will be added to the top of the list | `canEditSpace` |
| `PATCH` | `/card` | Update card from object in request body. Body object must contain `id`. `spaceId` cannot be patched | `canEditSpace` |
| `PATCH` | `/card/multiple` | Updates multiple cards from an array of objects in request body. Works just like `PATCH /card` | `canEditSpace` |
| `PATCH` | `/card/update-counter` | Increment or decrement a card counter for voting. Body object must contain `cardId`, and either `shouldIncrement: true` or `shouldDecrement: true` | None |
| `PATCH` | `/card/restore` | Restore removed card specified in body | `canEditSpace` |
| `DELETE` | `/card/list` | Remove card from the [List](#lists) that it's in. Body object must contain card `id`. The card's position will be shifted to the right of the list. | `canEditSpace` |
| `DELETE` | `/card` | Remove card specified in body | `canEditSpace` |
| `DELETE` | `/card/permanent` | Permanently remove card specified in body | `canEditSpace` |

### Card Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the card. Is not user updateable |
| `backgroundColor` | `String` | The background color for the card |
| `createdAt` | `String` | The date when the card was created |
| `codeBlockLanguage` | `String` | Code language syntax highlighting to use for markdown ` ``` ` code blocks |
| `counterIsVisible` | `Boolean` | Whether the card counter for voting is visible |
| `counterValue` | `Integer` | The incremented number of the card counter. Default value is `0` |
| `frameId` | `Integer` | The id of type of frame applied to the card, if any |
| `headerFontId` | `Integer` | An id representing the card's header font. Default value is `0` for Recoletta |
| `headerFontSize` | `String` | The header font size of the card. Can be either `s` (small-size, default), `m` (medium-size), or `l` (large-size) |
| `height` | `String` | The reference height of the card. Used to generate space preview images |
| `isCreatedThroughPublicApi` | `Boolean` | Whether the card was created through the public API. Cards that created through `POST /card/` will automatically receive this attribute |
| `isComment` | `Boolean` | Whether the card is a comment (an alternative to the `((comment))` name syntax) |
| `isLocked` | `Boolean` | Whether the card is locked and cannot be selected or edited in the client unless unlocked |
| `isRemoved` | `Boolean` | Whether the card has been soft-removed. (Can be restored or permanently removed by space users) |
| `isTodo` | `Boolean` | Whether the card has a checkbox (either completed `[x]` or uncompleted `[]`) |
| `linkToSpaceId` | `String` | The `spaceId` linked to in the card name |
| `linkToCardId` | `String` | The `cardId` linked to in the card name. A card link will always also include `linkToSpaceId` (but not vice versa) |
| `linkToSpaceCollaboratorKey` | `String` | The `collaboratorKey` used to invite someone to the space specified in `linkToSpaceId`. Indicates the the space has a space invite link |
| `maxWidth` | `Boolean` | Sets the default maximum width before cards text starts wrapping |
| `name` | `String` | The name of the card is its main text. Limited to 4000 characters |
| `nameUpdatedAt` | `String` | The date when the card name was last updated |
| `nameUpdatedByUserId` | `String` | The user id that last updated the name of the card |
| `resizeWidth` | `Integer` | The width of a card that's been manually resized by the user |
| `shouldHideUrlPreviewImage` | `Boolean` | Whether the card will display it's url preview image |
| `shouldHideUrlPreviewInfo` | `Boolean` | Whether the card will display it's url preview title and description |
| `shouldUpdateUrlPreview` | `Boolean` | Whether the card should be checked for a url preview the next time it's space is loaded in the kinopio-client app. This attribute is automatically assigned to cards created by /card POSTs |
| `spaceId` | `String` | The space that the card belongs to |
| `tilt` | `Integer` | The amount a card is rotated in degrees. Default value is `0` |
| `updatedAt` | `String` | The date when any changes in the card was made, including to it's position. Use `nameUpdatedAt` instead to see when the card name was changed |
| `urlIsVisible` | `Boolean` | Whether the url string is displayed on the card |
| `urlPreviewDescription` | `String` | The description displayed in the line of the url preview. Because most sites stuff their description tags with SEO gibberish, descriptions are only displayed for whitelisted domains. Contact support to add a domain to the whitelist. |
| `urlPreviewErrorUrl` | `String` | The last url that the preview failed on (could be a private or broken url). If this matches `urlPreviewUrl`, the url preview won't be created |
| `urlPreviewFavicon` | `String` | The url for the url preview favicon image |
| `urlPreviewImage` | `String` | The url for the url preview image |
| `urlPreviewIsVisible` | `Boolean` | Whether the card will display a url preview (aka link unfurl) |
| `urlPreviewTitle` | `String` | The title displayed in the url preview |
| `urlPreviewUrl` | `String` | The url that the card url preview is based on |
| `urlPreviewEmbedHtml` | `String` | `DEPRECATED` html embed code returned by iframely. Used to display url previews when available (like youtube videos). Html containing `<script>` tags is run inside an iframe. |
| `urlPreviewIframeUrl` | `String` | Iframe url returned by iframely. Used to display url previews when available (like youtube videos). Cannot be patched. |
| `videoIsPaused` | `Boolean` | Whether video file (mp4) playback in a card will be paused |
| `width` | `String` | The reference width of the card. Used to generate space preview images |
| `x` | `Integer` | The x-axis position |
| `y` | `Integer` | The y-axis position |
| `z` | `Integer` | The z-axis position |

## Connections

Connections are the lines that connect cards together. Connections have a `connection-type` which assigns them a color and allows the user to thematically group cards together by connected type.

### Connection Routes

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the connection belongs to.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/connection/   :connectionId` | Get info on a connection | None |
| `POST` | `/connection` | Create connection(s) from object in request body. Object must contain `spaceId`, `connectionTypeId` | `canEditSpace` |
| `PATCH` | `/connection` | Update connection(s) from object in request body. `spaceId` cannot be patched. | `canEditSpace` |
| `DELETE` | `/connection` | Permenently remove connection(s) speced in req body | `canEditSpace` |

### Connection Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the connection. Is not user updateable |
| `connectionTypeId` | `String` | The connection-type that the connection belongs to |
| `controlPoint` | `String` | Custom control point for a connection path curve. `q00,00` makes a straight line |
| `createdAt` | `String` | The date when the connection was created |
| `directionIsVisible` | `Boolean` | The connection has a directional arrow, in the direction of start card to end card |
| `endItemId` | `String` | The card or box that the connection line ends at |
| `labelIsVisible` | `Boolean` | The connection has a connection type label |
| `labelRelativePositionX` | `Float` | Label's `horizontal` position relative to the DOM box of it's parent connection. Is between `0` (max left) and `1` (max right). Default is `0.5` (middle) |
| `labelRelativePositionY` | `Float` | Label's `vertical` position relative to the DOM box of it's parent connection. Is between `0` (max top) and `1` (max bottom). Default is `0.5` (middle) |
| `path` | `String` | [SVG path](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths) that defines the connection line and its curve, e.g. 'm524,138 q90,40 49,123' is a quadratic bezier curve made up of origin XY, control point XY, and end XY points. |
| `point1Cardinal` | `String` | The cardinal direction used to connect to the `startItem`. Possible values are `north`, `south`, `west`, `east`, `northEast`, `southEast`, `southWest`, `northWest`. |
| `point2Cardinal` | `String` | Same as `point1Cardinal`, but for connecting to the `endItem` |
| `spaceId` | `String` | The space that the connection belongs to |
| `startItemId` | `String` | The card or box that the connection line starts from |
| `updatedAt` | `String` | The date when any changes to the connection were made |

## Connection Types

Connection Types group [Connections](#connections) together to allow the attributes of multiple connection lines to be represented and edited together.

### Connection Type Routes

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the connection type belongs to.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/connection-type/:connectionTypeId` | Get info on a connectionType | None |
| `POST` | `/connection-type` | Create connectionType(s) from object (or array) in request body. Object must contain `spaceId` | `canEditSpace` |
| `PATCH` | `/connection-type` | Update connectionType(s) from object in request body. `spaceId` cannot be patched. | `canEditSpace` |
| `DELETE` | `/connection-type` | Permenently remove connectionType | `canEditSpace` |

### Connection Type Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the connection. Is not user updateable |
| `color` | `String` | User color changes your paint stroke and default avatar color |
| `createdAt` | `String` | The date when the connection type was created |
| `name` | `String` | The name of the connection-type |
| `spaceId` | `String` | The space that the connection-type belongs to |
| `updatedAt` | `String` | The date when any changes were made to the connection type |

## Boxes

Boxes are items used by users to contain or organize cards in a space. They can be named, colored, and positioned

### Box Routes

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the box belongs to.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/box/:boxId` | Get info on a box | `canViewSpace` |
| `POST` | `/box` | Create a box from object in request body. Object must contain `spaceId` | `canEditSpace` |
| `PATCH` | `/box` | Update box from object in request body | `canEditSpace` |
| `DELETE` | `/box` | Permenently remove box, from object in request body | `canEditSpace` |

### Box Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the connection. Is not user updateable |
| `background` | `String` | The image url used by the box background |
| `backgroundIsStretch` | `Boolean` | Whether the box background image is stretched (default is `false`, to display images tiled) |
| `color` | `String` | The color of the box |
| `createdAt` | `String` | The date when the box was created |
| `headerFontId` | `Integer` | An id representing the header font of the box. Default value is `0` for Recoletta. Similar to `card.headerFontId` |
| `headerFontSize` | `String` | The header font size of the box. Can be either `s` (small-size, default), `m` (medium-size), or `l` (large-size). Similar to `card.headerFontSize` |
| `infoHeight` | `String` | The reference height of the box info area. Used to generate space preview images |
| `infoWidth` | `String` | The reference width of the box info area. Used to generate space preview images |
| `isLocked` | `Boolean` | Whether the box is locked and cannot be selected or edited in the client unless unlocked |
| `isTodo` | `Boolean` | Whether the box has a checkbox (either completed `[x]` or uncompleted `[]`) |
| `fill` | `String` | The fill type for the box. Possible values are `filled`, `empty` |
| `name` | `String` | The name of the box |
| `resizeHeight` | `String` | The height of the box |
| `resizeWidth` | `String` | The width of the box |
| `spaceId` | `String` | The space that the box belongs to |
| `userId` | `String` | The user that created the box |
| `updatedAt` | `String` | The date when any changes were made to the box |
| `x` | `Integer` | The x-axis position of the box origin (top-left point) |
| `y` | `Integer` | The y-axis position of the box origin |
| `z` | `Integer` | The z-axis position |

## Lists

Lists are items used by users to vertically contain and organize cards in a space. They can be named, colored, and positioned. [Cards](#cards) that belong to lists have a `listId`, and `listPositionIndex`.

### List Routes

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the list belongs to.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/list/:listId` | Get info on a list, including cards | `canViewSpace` |
| `POST` | `/list` | Create a list from object in request body. Body object must contain `spaceId` | `canEditSpace` |
| `PATCH` | `/list` | Update list from object in request body. Body object must contain `id` and `spaceId` | `canEditSpace` |
| `DELETE` | `/list/` | Permenently remove list in request body. Body object must contain `id` and `spaceId` | `canEditSpace` |

### List Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the list. Is not user updateable |
| `color` | `String` | The color of the list |
| `createdAt` | `String` | The date when the list was created |
| `name` | `String` | The name of the list |
| `height` | `String` | The rendered height of the list |
| `frameId` | `Integer` | The id of type of frame applied to the list, if any |
| `resizeWidth` | `String` | The width of the list |
| `shouldUpdateList` | `Boolean` | Whether the list dimensions, and the positions of the cards inside it, should be updated the next time the space is loaded. This is set automatically when adding cards to a list via the API. |
| `spaceId` | `String` | The space that the list belongs to |
| `userId` | `String` | The user that created the list |
| `updatedAt` | `String` | The date when any changes were made to the list |
| `x` | `Integer` | The x-axis position of the list origin (top-left point) |
| `y` | `Integer` | The y-axis position of the list origin |
| `z` | `Integer` | The z-axis position |

Each tag you add to a card is considered a seperate entity. So if you have two cards which both have the tag \[\[balloon\]\], this is two tag entities both named 'balloon', with different cardIds.

Routes with Auth `canEditSpace` requires that your Authorization apiKey belongs to a user with the permission to edit the space that the tag belongs to.

## Notifications

Notifications are created when another user adds a card in a space that you're a member and not currently viewing. The notifying user can be either a space collaborator, or anyone viewing an open space.

### Notifications Routes

Routes with Auth as `apiKey` mean that the Authorization header apiKey must match the requested user.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/notifications` | Get the last 50 notifications for the current user | `apiKey` |

### Notifications Attributes

| Name | Type | Description |
| --- | --- | --- |
| `id` | `String` | The unique ID of the notification. Is not user updateable |
| `card` | `Object` | Basic information about the [Card](#cards) `id`, `name` |
| `cardId` | `String` | The card that the notification involves |
| `createdAt` | `String` | The date when the notification was created |
| `isEmailed` | `Boolean` | Has the notification been emailed to the recipient. Emails are only sent if `user.shouldEmailNotifications = true` |
| `isRead` | `Boolean` | Has the notification been read by the recipient in Kinopio |
| `recipientUserId` | `String` | The user that'll receive the notification |
| `space` | `Object` | Basic information about the [Space](#spaces) `id`, `name`, `privacy`, `background` |
| `spaceId` | `String` | The space that the notification involves |
| `type` | `String` | The action that created the notification (e.g. `addCard`) |
| `user` | `Object` | Basic information about the [User](#users) `id`, `name`, `color` |
| `userId` | `String` | The user that created the notification |
| `updatedAt` | `String` | The date when any changes were made to the notification |

## Other

Other routes used by the kinopio-client app, which you can also use in your integrations

### other Routes

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/affiliate` | returns affiliate info, promo url, commissions earned, and pending payout | `AffiliateUser` |
| `GET` | `/services/community-backgrounds` | Lists the space background images aded to the [are.na channel](https://www.are.na/kinopio/community-backgrounds) | None |
| `GET` | `/meta/date` | Current time/timezone of kinopio-server | None |
| `GET` | `/meta/changelog` | Lists recent Kinopio new feature updates | None |
| `GET` | `/meta/emojis` | List of [unicode emojis](https://github.com/muan/unicode-emoji-json/blob/main/data-by-group.json) for the emoji picker | None |
| `GET` | `/meta/random-name` | returns a random word space name – based on the logic formerly used to generate space names | None |