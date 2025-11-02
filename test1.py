import semantic_version as sv


class VersionCanNoPatch(sv.Version):
    """
    支持不带patch版本号的版本类，兼容semantic_version.Version的参数
    """
    def __init__(
        self,
        version_string=None,
        major=None,
        minor=None,
        patch=None,
        prerelease=None,
        build=None,
        partial=False
    ):
        # 保存原始版本字符串
        self._original_version = version_string
        
        # 如果提供了单独的版本组件参数，则使用父类的构造方式
        if major is not None or minor is not None or patch is not None:
            super().__init__(
                version_string=version_string,
                major=major,
                minor=minor,
                patch=patch,
                prerelease=prerelease,
                build=build
            )
        else:
            # 如果是不带patch的版本格式，补全为带patch的格式
            normalized_version = self._normalize_version(version_string)
            # 调用父类初始化，不传递partial参数
            super().__init__(normalized_version)
    
    def _normalize_version(self, version_string):
        """
        将不带patch的版本号标准化为带patch的版本号
        """
        # 处理None值
        if version_string is None:
            return None
            
        # 分离版本主体和预发布/构建部分
        # 处理预发布版本标识
        if '-' in version_string:
            version_part, suffix_part = version_string.split('-', 1)
            suffix_part = f"-{suffix_part}"
        else:
            version_part = version_string
            suffix_part = ""
            
        # 处理构建版本标识
        if '+' in version_part:
            version_part, build_part = version_part.split('+', 1)
            build_part = f"+{build_part}"
        else:
            build_part = ""
        
        # 检查版本号部分是否缺少patch
        version_components = version_part.split('.')
        if len(version_components) == 2:
            # 补全patch版本号为0
            version_part = f"{version_part}.0"

        return f"{version_part}{suffix_part}{build_part}"

# 测试用例
if __name__ == "__main__":
    # 测试不带patch的版本
    ver1 = VersionCanNoPatch('3.6')
    print(f"Version '3.6' patch: {ver1.patch}")  # 输出: 0
    
    # 测试带预发布标识的版本
    ver2 = VersionCanNoPatch('3.6-Rel')
    print(f"Version '3.6-Rel' patch: {ver2.patch}")  # 输出: 0
    
    # 测试正常的完整版本号
    ver3 = VersionCanNoPatch('3.6.1')
    print(f"Version '3.6.1' patch: {ver3.patch}")  # 输出: 1
    
    # 测试带预发布和构建信息的版本
    ver4 = VersionCanNoPatch('3.6-rc1+build.1')
    print(f"Version '3.6-rc1+build.1' patch: {ver4.patch}")  # 输出: 0

# 测试用例
ver = VersionCanNoPatch('3.6.0-Rel')
print(ver.patch)  # 输出: 0