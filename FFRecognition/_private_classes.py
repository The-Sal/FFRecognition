import json

class Transferable:
    def __init__(self):
        pass

    def transferable(self):
        self_dict = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, Transferable):
                self_dict[key] = value.transferable()
            else:
                self_dict[key] = value

        return json.dumps(self_dict, indent=4)

    @classmethod
    def from_transferable(cls, transferable: str):
        self_dict = json.loads(transferable)
        self = cls.__new__(cls)
        for key, value in self_dict.items():
            if isinstance(value, dict):
                self_dict[key] = cls.from_transferable(json.dumps(value))
        self.__dict__ = self_dict
        return self




# Src:
# struct BATCH_ImagePaths: Codable{
#     var paths: [String]
# }
class Batch_ImagePaths(Transferable):
    def __init__(self, paths: list):
        super().__init__()
        self.paths = paths

# Src:
# struct BATCH_ImageIds: Codable{
#     var ids: [Int]
# }
class Batch_ImageIds(Transferable):
    def __init__(self, ids: list):
        super().__init__()
        self.ids = ids

# Srcs:
# struct BATCH_FaceImagesRAW64: Codable{
#     var array: [FaceImagesRAW64]
# }
class Batch_FaceImagesRAW64(Transferable):
    def __init__(self, array: list):
        super().__init__()
        self.array = array
        self._images_datas = self._fromArray(array)

    @property
    def faces_for_image(self):
        return self._images_datas

    @classmethod
    def from_transferable(cls, transferable: str):
        self_dict = json.loads(transferable)
        self = cls.__new__(cls)
        self.__dict__ = self_dict
        self._images_datas = Batch_FaceImagesRAW64._fromArray(self_dict['array'])
        return self


    @staticmethod
    def _fromArray(array: list):
        from .classes import Swift_FaceImage
        _images = []
        for item in array:
            sub_faces = []
            for face_raw in item['faces']:
                sub_faces.append(Swift_FaceImage(face_raw))

            _images.append(sub_faces)

        return _images



