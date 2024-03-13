import 'package:core/core.dart';
import 'package:domain/domain.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

// required: associates our `model00001a.dart` with the code generated
// by freezed
part 'model00001a.freezed.dart';
// optional: since our [Model00001a] class is serialisable,
// we must add this line. but if [Model00001a] was not serialisable,
// we could skip it.
part 'model00001a.g.dart';

/// {@template Model00001a}
/// Add documentation here
///
/// Describe what is the model purpose
/// {@endtemplate}
@freezed
class Model00001a with _$Model00001a implements EntityMapper<Aaa> {
  /// {@macro Model00001a}
  const factory Model00001a() = _Model00001a;

  /// For custom getters and methods to work. Must not have any parameter.
  // ignore: unused_element
  const Model00001a._();

  /// Converts the [json] data to an instance of this object.
  factory Model00001a.fromJson(Map<String, Object?> json) =>
      _$Model00001aFromJson(json);

  @override

  /// Converts the model to entity to be use in the application
  Aaa toEntity() {
    return const Aaa();
  }
}
