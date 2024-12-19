import { createCommonFetchOptions, mergeFetchOptions, type CommonFetchOptions } from '~/utils/api'

export function useApi() {
  const config = useRuntimeConfig()
  const baseOptions = createCommonFetchOptions(config)

  async function fetchApi<T>(url: string, options: Partial<CommonFetchOptions> = {}): Promise<T> {
    const finalOptions = mergeFetchOptions(baseOptions, options)
    return await $fetch<T>(url, finalOptions)
  }

  return {
    fetchApi
  }
}
