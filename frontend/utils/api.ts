import { getCSRFToken } from './csrf'
import type { FetchOptions } from 'ofetch'

export type HTTPMethod = 
  | 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  | 'HEAD' | 'OPTIONS' | 'CONNECT' | 'TRACE'
  | 'get' | 'post' | 'put' | 'delete' | 'patch'
  | 'head' | 'options' | 'connect' | 'trace'

export interface CommonFetchOptions extends FetchOptions {
  baseURL: string
  credentials: RequestCredentials
  method?: HTTPMethod
  headers: {
    'Accept': string
    'Content-Type': string
    'X-CSRFToken': string
    [key: string]: string
  }
}

/**
 * Creates a standardised set of fetch options for API requests.
 * This function ensures consistent configuration across all API calls,
 * including proper CSRF token handling and content type headers.
 * 
 * @param config - The runtime config object from useRuntimeConfig()
 * @returns CommonFetchOptions object with all necessary API request settings
 */
export function createCommonFetchOptions(config: ReturnType<typeof useRuntimeConfig>): CommonFetchOptions {
  return {
    baseURL: config.public.apiBaseUrl,
    credentials: 'include' as RequestCredentials,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    }
  }
}

/**
 * Merges custom options with the common fetch options.
 * This is useful when you need to add or override specific options
 * while maintaining the base configuration.
 * 
 * @param commonOptions - The base fetch options from createCommonFetchOptions
 * @param customOptions - Additional options to merge with the base options
 * @returns Merged fetch options
 */
export function mergeFetchOptions(
  commonOptions: CommonFetchOptions, 
  customOptions: Partial<CommonFetchOptions> = {}
): CommonFetchOptions {
  return {
    ...commonOptions,
    ...customOptions,
    headers: {
      ...commonOptions.headers,
      ...(customOptions.headers || {})
    }
  }
}
