import { isArray } from 'lodash';
import { isDateTime } from 'vega-lite/build/src/datetime';
import {
  LogicalAnd,
  LogicalComposition,
  LogicalOr,
  forEachLeaf,
  isLogicalNot
} from 'vega-lite/build/src/logical';
import {
  FieldEqualPredicate,
  FieldRangePredicate,
  Predicate,
  isFieldPredicate
} from 'vega-lite/build/src/predicate';
import {
  SelectionInitIntervalMapping,
  SelectionInitMapping,
  SelectionParameter,
  isSelectionParameter
} from 'vega-lite/build/src/selection';
import { FilterTransform, Transform } from 'vega-lite/build/src/transform';
import { Interactions } from '../../interactions/types';
import { objectToKeyValuePairs } from '../../utils/objectToKeyValuePairs';
import { VegaLiteSpecProcessor } from './processor';
import { isSelectionInterval, removeParameterValue } from './selection';
import { isPrimitiveValue } from './spec';
import { AnyUnitSpec } from './view';

export const OUT_FILTER_LAYER = '__OUT_FILTER_LAYER__';
export const IN_FILTER_LAYER = '__IN_FILTER_LAYER__';

export type Filter = LogicalComposition<Predicate>;
export type FilterDirection = 'in' | 'out';

const NON_NULL_FORCE_STRING = '__NON_NULL_FORCE_STRING__';

/**
 * @param vlProc - processor object
 * @returns processor object
 *
 * NOTE: filter operations only adds one layer
 */
export function applyFilter(
  vlProc: VegaLiteSpecProcessor,
  filterAction: Interactions.FilterAction
): VegaLiteSpecProcessor {
  const { direction } = filterAction;

  const baseLayerId = OUT_FILTER_LAYER;

  // get all params
  const { params } = vlProc;

  const selections = params.filter(isSelectionParameter);

  const filterPredicates = getFiltersFromSelections(selections);

  const combinedPredicate = createLogicalOrPredicate(filterPredicates);

  vlProc.updateTopLevelParameter(param =>
    isSelectionParameter(param) ? removeParameterValue(param) : param
  );

  // should be and?
  vlProc.addLayer(baseLayerId, spec =>
    addFilterTransform(
      spec,
      direction === 'out' ? invertFilter(combinedPredicate) : combinedPredicate
    )
  );

  return vlProc;
}

export function addFilterTransform(
  spec: AnyUnitSpec,
  filter: Filter
): AnyUnitSpec {
  const { transform = [] } = spec;

  const filterTransform = createFilterTransform(filter);

  transform.push(filterTransform);

  spec.transform = transform;

  return spec;
}

export function getFiltersFromSelections(
  selections: SelectionParameter[]
): Filter[] {
  const filters = selections
    .map(selection => getFiltersFromSelection(selection))
    .flat();

  return filters;
}

export function getFiltersFromSelection(
  selection: SelectionParameter
): Filter[] {
  const value = selection.value;

  const filters: Filter[] = [];

  if (isPrimitiveValue(value) || isDateTime(value)) {
    // TODO: Figure out what to do?
    throw new Error(`Cannot handle: ${value}`);
  } else if (isArray(value)) {
    const predicates = value.map(createFEPredicates).flat();

    filters.push(...predicates);
  } else if (typeof value === 'object') {
    const rangePredicates = createFRPredicate(value);

    const finalPredicates = isSelectionInterval(selection)
      ? [createLogicalAndPredicate(rangePredicates)]
      : rangePredicates;

    filters.push(...finalPredicates);
  }

  return filters;
}

export function invertFilter(predicate: Filter): Filter {
  return isLogicalNot(predicate)
    ? predicate.not
    : {
        not: predicate
      };
}

/**
 * @param selection - a vegalite selection mapping
 * @returns array of filter range predicates for each selection in the mapping
 */
function createFRPredicate(
  selection: SelectionInitIntervalMapping
): FieldRangePredicate[] {
  const selections = objectToKeyValuePairs(selection);

  return selections.map(({ key, value }) => ({
    field: key,
    range: value as any
  }));
}

/**
 * @param selection - a vegalite selection mapping
 * @returns array of filter equal predicates for each selection in the mapping
 *
 * **NOTE** - currently assumes all values in `selection` are non-null, so replacing value with `NON_NULL_FORCE_STRING`
 */
function createFEPredicates(
  selection: SelectionInitMapping
): FieldEqualPredicate[] {
  return objectToKeyValuePairs(selection).map(
    ({ key, value = NON_NULL_FORCE_STRING }) => ({
      field: key,
      equal: value as any
    })
  );
}

function createFilterTransform(
  filterPredicate: LogicalComposition<Predicate>
): FilterTransform {
  return {
    filter: filterPredicate
  };
}

export function createLogicalAndPredicate(
  predicates: Array<LogicalComposition<Predicate>>
): LogicalAnd<Predicate> {
  return {
    and: predicates
  };
}

export function createLogicalOrPredicate(
  predicates: Array<LogicalComposition<Predicate>>
): LogicalOr<Predicate> {
  return {
    or: predicates
  };
}

// NOTE: Doesn't do anything. check
export function mergeFilters(
  transform: Transform[],
  _logical: 'and' | 'or' = 'or'
): Transform[] {
  return transform;
}

export function extractFilterFields(
  filters: FilterTransform | FilterTransform[]
) {
  filters = isArray(filters) ? filters : [filters];

  const fields: string[] = [];

  filters.forEach(f => {
    forEachLeaf(f.filter, predicate => {
      if (isFieldPredicate(predicate)) {
        fields.push(predicate.field);
      }
    });
  });

  return [...new Set(fields)];
}
