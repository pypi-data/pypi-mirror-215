<template>
  <div>
    <MissionDetails :is-loading="isLoading" class="mb-3" :validation-info="v$?.form" />
    <MissionItinerary :is-loading="isLoading" :validation-info="v$?.form" />
    <div class="pb-[3.75rem]">
      <UButton :class="[$style['ops-page-wrapper__btn']]" :loading="isLoading" @click="onValidate">
        <span>Submit mission</span>
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import MissionDetails from '@/components/forms/sections/MissionDetails.vue'
import MissionItinerary from '@/components/forms/sections/MissionItinerary.vue'
import UButton from '@/components/ui/form/UButton.vue'
import { storeToRefs } from 'pinia'
import { useMissionFormStore } from '@/stores/useMissionFormStore'
import useVuelidate from '@vuelidate/core'
import { useFetch } from '@/composables/useFetch'
import type { Nullable } from '@/types/generic.types'
import type { IMission } from '@/types/mission/mission.types'
import Mission from '@/services/mission/mission'
import { rules } from '@/utils/rulesForForms'
import { useMissionStore } from '@/stores/useMissionStore'
import { computed, onMounted } from 'vue'
import { getIsLocalEnv, getMissionId } from '@/helpers'
import { notify } from '@/helpers/toast'
import { AxiosError } from 'axios'

const missionFormStore = useMissionFormStore()
const missionStore = useMissionStore()
const { formModel: missionForm } = storeToRefs(missionFormStore)
const { isUpdatingMission } = storeToRefs(missionStore)

const v$ = useVuelidate(rules(missionForm), { form: missionForm.value })

const {
  loading: isCreatingMission,
  data: createdMissionData,
  callFetch: createMission,
  error
} = useFetch(async (payload: Nullable<IMission>) => {
  const res = await Mission.create(payload)
  notify('Mission created successfully!', 'success')
  return res
})

const isLoading = computed(() => isCreatingMission?.value || isUpdatingMission?.value)

onMounted(() => {
  getMissionId() && missionStore.fetchMission(getMissionId() as number)
})

const missionActions = async () => {
  return getMissionId()
    ? await missionStore.updateMission(getMissionId() as number, missionForm.value)
    : await createMission(missionForm.value as any)
}

const onValidate = async () => {
  try {
    const isValid = await v$?.value?.$validate()
    if (!isValid) {
      return notify('Error while submitting, form is not valid!', 'error')
    } else {
      await missionActions()
      redirectToURL()
    }
  } catch (error) {
    const errorKeys = Object.keys(error.response?.data?.errors)
    if (errorKeys.length && errorKeys.some((key) => Number.isNaN(+key))) {
      errorKeys.forEach((key: any) => {
        ;(error as AxiosError<{ errors: string[] }>).response?.data.errors[key].forEach((err) => {
          const checkIfTextExist = err.detail?.length
          const formatText = checkIfTextExist ? err.detail : 'Something went wrong'
          notify(`${formatString(key)}: ${formatText}`, 'error')
        })
      })
    } else {
      const errors = (error as AxiosError<{ errors: string[] }>).response?.data?.errors?.toString()
      notify(errors, 'error')
    }
  }
}
const redirectToURL = () => {
  let url = ''
  getIsLocalEnv() ? (url = '/ops/missions/0/') : (url = window.redirect_uri)
  if (createdMissionData.value.data.id && url) {
    const redirectedId = (createdMissionData.value.data as IMission).id
    const redirectUrl = url.replace(/\d/, String(redirectedId))
    location.replace(redirectUrl)
  }
}

const formatString = (str: string) => {
  const removedUnderscore = str.replace(/_/g, ' ')
  return removedUnderscore[0].toUpperCase() + removedUnderscore.slice(1)
}
</script>

<style lang="scss" module>
.ops {
  &-page-wrapper {
    @apply flex justify-between items-center gap-2 mb-4;

    &__btn {
      @apply flex shrink-0 focus:shadow-none text-white bg-grey-900 mb-0 mt-2 p-2 px-4 #{!important};

      img {
        @apply w-5 h-5 mr-2;
        filter: invert(36%) sepia(14%) saturate(1445%) hue-rotate(190deg) brightness(93%)
          contrast(84%);
      }
    }

    &__content {
      @apply pr-0 sm:pr-4 sm:mr-[-1rem] relative;
    }
  }
}
</style>
