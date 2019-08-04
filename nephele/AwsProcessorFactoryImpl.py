from nephele import AwsAutoScalingGroup
from nephele import AwsLogGroup
from nephele import AwsRole
from nephele import AwsStack
from nephele import AwsEni

class AwsProcessorFactoryImpl:
    def AutoScalingGroup(self,scalingGroup,parent):
        # reload(AwsAutoScalingGroup)
        return AwsAutoScalingGroup.AwsAutoScalingGroup(scalingGroup,parent)

    def Eni(self,physicalId,parent):
        # reload(AwsEni)
        return AwsEni.AwsEni(physicalId,parent)

    def Stack(self,stack,logicalName,parent):
        # reload(AwsStack)
        return AwsStack.AwsStack(stack,logicalName,parent)

    def LogGroup(self,logGroupId,parent):
        # reload(AwsLogGroup)
        return AwsLogGroup.AwsLogGroup(logGroupId,parent)

    def Role(self,roleId,parent):
        # reload(AwsRole)
        return AwsRole.AwsRole(roleId,parent)
