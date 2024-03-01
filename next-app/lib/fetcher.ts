const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function fetcher(
    endpoint: string,
    queryParams: Object = {},
    options: RequestInit = {}
  ) {
    const opts: RequestInit = {
      cache: 'no-cache',
      credentials: 'include',
      ...options,
    }

    // Create a new URL object with the endpoint
    const url = new URL(endpoint, API_URL)

    if (queryParams) {
      // Convert non-string query parameters to strings
      const stringifiedQueryParams = Object.fromEntries(
        Object.entries(queryParams).map(([key, value]) => [key, String(value)])
      )
  
      // Add query parameters to the URL object using URLSearchParams
      const searchParams = new URLSearchParams(stringifiedQueryParams)
      url.search = searchParams.toString()
    }
  
    // Fetch data using the URL object with query parameters
    const response = await fetch(url, opts)
    
    let data
    if (response.status !== 204) {
      data = await response.json()
    }
    return { data: data, status: response.status }
}