export type AnyObject = {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    [key: string]: any;
  };
  
  type CaseConverter = (str: string) => string;
  
  /**
   * Converts a string from snake to camel case.
   */
  export const snakeToCamelCase: CaseConverter = (str: string): string =>
    str.replace(/([-_][a-z])/g, group =>
      group.toUpperCase().replace('-', '').replace('_', '')
    );
  
  /**
   * Converts a string from camel to snake case.
   */
  export const camelToSnakeCase: CaseConverter = (str: string): string =>
    str.replace(/([A-Z])/g, group => `_${group.toLowerCase()}`);
  
  /**
   * Converts the keys of an object to the given case.
   * using the given case converter function.
   */
  export const convertKeysCasing =
  <R extends AnyObject>(caseConverter: CaseConverter) =>
  (obj: AnyObject | AnyObject[]): R => {
    if (Array.isArray(obj))
      return obj.map(item =>
        typeof item === 'object'
          ? convertKeysCasing<R>(caseConverter)(item)
          : item
      ) as unknown as R;

    return Object.entries(obj).reduce((converted: AnyObject, [key, value]) => {
      const convertedKey = caseConverter(key);
      // Handle specific keys like endTime
      if (convertedKey === 'endTime' && value === null) {
        converted[convertedKey] = '';
      } else {
        converted[convertedKey] =
          value && typeof value === 'object'
            ? Array.isArray(value)
              ? value.map(item =>
                  typeof item === 'object'
                    ? convertKeysCasing(caseConverter)(item)
                    : item
                )
              : convertKeysCasing(caseConverter)(value)
            : value;
      }

      return converted;
    }, {}) as R;
  };
  
  /**
   * Converts the keys of an object from snake to camel case.
   */
  export const convertKeysFromSnakeToCamelCase = <R extends AnyObject>(
    obj: AnyObject | AnyObject[]
  ): R => convertKeysCasing<R>(snakeToCamelCase)(obj);
  
  /**
   * Converts the keys of an object from camel to snake case.
   */
  export const convertKeysFromCamelToSnakeCase = <R extends AnyObject>(
    obj: AnyObject | AnyObject[]
  ): R => convertKeysCasing<R>(camelToSnakeCase)(obj);
  