import client from './client'

interface TableParams {
  type: string
  label: string
  startDate?: string
  endDate?: string
  page?: number
  page_size?: number
  sort_by?: string
  sort_order?: string
}

interface DocumentResponse {
  id: number
  eo_number?: string
  name?: string
  title?: string
  document_date?: string
  date_of_publication?: string
  date_of_signing?: string
  pages_count?: number
  signatory_authority_id?: string
  type_name?: string
  region_name?: string
  district_name?: string
}

interface TableResponse {
  documents: DocumentResponse[]
  total_count: number
  page: number
  page_size: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

interface ApiResponse {
  data: TableResponse
  message: string
  status: number
}

class Table {
  endpoint: string

  constructor(endpoint = '/api/table') {
    this.endpoint = endpoint
  }

  /**
   * Получение документов для таблицы с фильтрацией и пагинацией
   */
  getDocuments = async (params: TableParams): Promise<ApiResponse> => {
    return (await client.get(`${this.endpoint}`, { params })).data
  }

  /**
   * Получение доступных типов фильтров
   */
  getFilters = async () => {
    return (await client.get(`${this.endpoint}/filters`)).data
  }
}

export default Table
