import { Field, isFieldDef } from 'vega-lite/build/src/channeldef';
import { Encoding, fieldDefs } from 'vega-lite/build/src/encoding';
import { Nullable } from '../../utils';

export function getFieldNamesFromEncoding(
  encoding: Encoding<Field>,
  keys: Array<keyof Encoding<Field>>
) {
  const map = keys
    .map(k => {
      const f = encoding[k];
      if (isFieldDef(f) && f.field) {
        return {
          [k]: f.field
        } as { [K in keyof Encoding<Field>]: Encoding<Field>[K] };
      }
    })
    .filter(k => !!k)
    .reduce((acc, o) => {
      return { ...acc, ...o };
    }, {});

  return map;
}

export function getFieldsFromEncoding(encoding: Encoding<Field>) {
  const val = fieldDefs(encoding);

  return val;
}

export function addEncoding<K extends keyof Encoding<Field>>(
  encoding: Nullable<Encoding<Field>>,
  name: K,
  value: Encoding<Field>[K]
) {
  encoding = encoding || {};

  return {
    ...encoding,
    [name]: value
  };
}

export function removeEncoding<K extends keyof Encoding<Field>>(
  encoding: Nullable<Encoding<Field>>,
  name: K
) {
  encoding = encoding || {};

  delete encoding[name];

  return encoding;
}
