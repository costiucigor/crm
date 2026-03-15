<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Integrations" />
      </template>
    </LayoutHeader>

    <div class="p-5 overflow-y-auto">
      <div v-if="!isManager()" class="text-ink-gray-5">
        {{ __('You do not have permission to access this page.') }}
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-4 rounded border border-outline-gray-2 bg-surface-white">
          <div class="text-base font-medium text-ink-gray-9">
            {{ __('WhatsApp') }}
          </div>
          <div class="mt-1 text-sm text-ink-gray-6">
            {{ __('Configure WhatsApp messaging integration.') }}
          </div>
          <div class="mt-4">
            <Button
              variant="solid"
              :label="__('Open Settings')"
              @click="openSettings('WhatsApp')"
            />
          </div>
        </div>

        <div class="p-4 rounded border border-outline-gray-2 bg-surface-white">
          <div class="text-base font-medium text-ink-gray-9">
            {{ __('IP Telephony') }}
          </div>
          <div class="mt-1 text-sm text-ink-gray-6">
            {{ __('Configure call integration and call logs.') }}
          </div>
          <div class="mt-4">
            <Button
              variant="solid"
              :label="__('Open Settings')"
              @click="openSettings('Telephony')"
            />
          </div>
        </div>

        <div class="p-4 rounded border border-outline-gray-2 bg-surface-white">
          <div class="text-base font-medium text-ink-gray-9">
            {{ __('Lead Webhook') }}
          </div>
          <div class="mt-1 text-sm text-ink-gray-6">
            {{ __('Create leads by sending a POST request from your website.') }}
          </div>
          <div class="mt-3 text-xs font-mono p-2 rounded bg-surface-gray-2 text-ink-gray-8">
            /api/method/crm.api.leads_webhook.webhook
          </div>
          <div class="mt-3 text-sm text-ink-gray-6">
            {{ __('Optional header: X-CRM-Webhook-Secret') }}
          </div>
        </div>

        <div class="p-4 rounded border border-outline-gray-2 bg-surface-white">
          <div class="text-base font-medium text-ink-gray-9">
            {{ __('Lead Syncing') }}
          </div>
          <div class="mt-1 text-sm text-ink-gray-6">
            {{ __('Configure lead syncing sources (e.g. Facebook Lead Ads).') }}
          </div>
          <div class="mt-4">
            <Button
              variant="solid"
              :label="__('Open Settings')"
              @click="openSettings('Lead Syncing')"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import { showSettings, activeSettingsPage } from '@/composables/settings'
import { usersStore } from '@/stores/users'
import { Button } from 'frappe-ui'

const { isManager } = usersStore()

function openSettings(page) {
  showSettings.value = true
  activeSettingsPage.value = page
}
</script>

