## Table `users`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `uuid` | Primary |
| `username` | `text` |  |
| `created_at` | `timestamptz` |  Nullable |
| `is_deleted` | `bool` |  |
| `deleted_at` | `timestamptz` |  Nullable |

## Table `lost_items`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int8` | Primary Identity |
| `title` | `text` |  |
| `description` | `text` |  Nullable |
| `category` | `text` |  |
| `location` | `text` |  Nullable |
| `lost_date` | `text` |  Nullable |
| `status` | `text` |  Nullable |
| `created_at` | `timestamptz` |  Nullable |
| `user_id` | `uuid` |  Nullable |
| `tags` | `_text` |  |

## Table `lost_item_images`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int8` | Primary Identity |
| `lost_item_id` | `int8` |  |
| `image_path` | `text` |  |
| `created_at` | `timestamptz` |  Nullable |

## Table `bookmarks`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int8` | Primary Identity |
| `user_id` | `uuid` |  |
| `item_id` | `int8` |  |

## Table `chats`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int8` | Primary Identity |
| `item_id` | `int8` |  |
| `user_id` | `uuid` |  |
| `message` | `text` |  |
| `timestamp` | `timestamptz` |  Nullable |
| `room_id` | `int8` |  |
| `receiver_id` | `uuid` |  |

## Table `chat_rooms`

### Columns

| Name | Type | Constraints |
|------|------|-------------|
| `id` | `int8` | Primary Identity |
| `item_id` | `int8` |  |
| `user1_id` | `uuid` |  |
| `user2_id` | `uuid` |  |
| `created_at` | `timestamptz` |  |

## RLS Policies

### `chat_rooms`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Participants can create chat rooms` | INSERT | authenticated | PERMISSIVE | — | `((auth.uid() = user1_id) OR (auth.uid() = user2_id))` |
| `Participants can view chat rooms` | SELECT | authenticated | PERMISSIVE | `((auth.uid() = user1_id) OR (auth.uid() = user2_id))` | — |

### `chats`

| Policy | Command | Roles | Action | USING | WITH CHECK |
|--------|---------|-------|--------|-------|------------|
| `Participants can send messages` | INSERT | authenticated | PERMISSIVE | — | `((auth.uid() = user_id) AND (EXISTS ( SELECT 1    FROM chat_rooms r   WHERE ((r.id = chats.room_id) AND (((auth.uid() = r.user1_id) AND (chats.receiver_id = r.user2_id)) OR ((auth.uid() = r.user2_id) AND (chats.receiver_id = r.user1_id)))))))` |
| `Participants can view messages` | SELECT | authenticated | PERMISSIVE | `(EXISTS ( SELECT 1    FROM chat_rooms r   WHERE ((r.id = chats.room_id) AND ((auth.uid() = r.user1_id) OR (auth.uid() = r.user2_id)))))` | — |

