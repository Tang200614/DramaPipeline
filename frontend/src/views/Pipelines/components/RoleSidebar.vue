<!-- 流水线角色列表 -->
<!-- @author fortune -->
<!-- @date 2026-03-19 -->

<template>
  <aside class="pipeline-roles-sidebar">
    <div class="roles-header">
      <span class="roles-title">流水线角色</span>
      <span class="roles-count">{{ roles.length }} 个</span>
    </div>
    <ul class="roles-list">
      <li
        v-for="role in roles"
        :key="role.id"
        class="role-item"
        :class="{
          'role-active': role.status === 'active',
          'role-done': role.status === 'done',
          'role-pending': role.status === 'pending',
        }"
        @click="$emit('select', role)"
      >
        <span class="role-icon">
          <template v-if="role.status === 'done'">✓</template>
          <template v-else-if="role.status === 'active'">
            <span class="icon-sync">⟳</span>
          </template>
          <template v-else>⏳</template>
        </span>
        <span class="role-label">{{ role.name }}</span>
        <span class="role-badge" :class="`badge-${role.status}`">
          {{ statusText(role.status) }}
        </span>
      </li>
    </ul>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  roles: { id: string; name: string; status: 'done' | 'active' | 'pending' }[]
}>()
defineEmits<{ select: [role: { id: string; name: string; status: 'done' | 'active' | 'pending' }] }>()

function statusText(s: string) {
  const map: Record<string, string> = {
    done: '已完成',
    active: '进行中',
    pending: '待执行',
  }
  return map[s] ?? s
}
</script>

<style scoped>
.pipeline-roles-sidebar {
  width: 260px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--dp-border-subtle);
  background: var(--dp-bg-secondary);
}

.roles-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  font-size: 0.75rem;
  color: var(--dp-text-muted);
}

.roles-title {
  font-weight: 600;
  color: var(--dp-text-secondary);
}

.roles-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 0.75rem 1rem;
  list-style: none;
}

.role-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  margin-bottom: 0.25rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.role-item:hover {
  background: rgba(0, 128, 255, 0.06);
}

.role-active {
  background: rgba(0, 128, 255, 0.12);
}

.role-done .role-icon { color: #22c55e; }
.role-pending .role-icon { color: var(--dp-text-muted); }
.role-active .role-icon { color: #0080ff; }

.icon-sync {
  display: inline-block;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.role-label {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--dp-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-badge {
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  text-transform: uppercase;
}

.badge-done {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.badge-active {
  background: rgba(0, 128, 255, 0.2);
  color: #0080ff;
}

.badge-pending {
  background: rgba(100, 116, 139, 0.2);
  color: var(--dp-text-muted);
}
</style>
